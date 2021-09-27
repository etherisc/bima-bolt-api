import datetime
import json
import logging
import math
import uuid

from base.model import BaseClass, Entity
from repository.mongodb_collection import ID_ATTRIBUTE_MONGO
from util.json_encoder import DateTimeEncoder
from util.geo import pixel_to_latitude_longitude

from entity.arc2 import Rainfall, RainfallCalculator

from entity.constants import POLICY_STATUS_PENDING, POLICY_STATUS_ACTIVE, POLICY_STATUS_COMPLETED
from entity.constants import COVERAGE_GERMINATION_DRY, COVERAGE_GERMINATION_WET, COVERAGE_VEGETATION, COVERAGE_FLOWERING, COVERAGE_EXCESS_RAIN
from entity.constants import STAGE_STATUS_PENDING, STAGE_STATUS_SCHEDULED, STAGE_STATUS_COMPLETED

from entity.policy_template import GroupPolicyTemplate
from entity.policy_template import CropStageConfiguration

from entity.schema.crop_stage_schema import CropStageSchema
from entity.schema.group_policy_schema import GroupPolicySchema
from entity.schema.schemas import validate_object

from util.timestamp import LocalizedTimeStamp, LocalDate

class GroupPolicy(Entity):

    # TODO get rid of parameter sow_window
    def __init__(self, *args):
        super().__init__()

        # default
        if len(args) in [3,4]:
            business_tx_id = args[0]
            task_id = args[1]
            group_policy_template = args[2]
            sow_window=None

            if len(args) == 4:
                sow_window = args[3]
        
        # should only be called by method from_dict
        elif len(args) == 0:
            return

        # should never happen
        else:
            logging.error("unsupported list for GroupPolicy constructor {}".format(args))
            return
        
        self['id'] = group_policy_template['id']
        self['template'] = group_policy_template

        self['season'] = group_policy_template['season']
        self['crop'] = group_policy_template['crop']
        self['activation_window'] = group_policy_template['activation_window']

        self['sow_window'] = sow_window
        self['begin_date'] = None
        self['end_date'] = None

        self['crop_stages'] = self._populate_crop_stages()

        self['payout'] = {
            'hurdle': self._get_hurdle(),
            'deductible': self._get_deductible(),
            'maximum': group_policy_template['max_payout'],
            'minimum': group_policy_template['min_payout'],
            'total': 0.0,
            'actual': 0.0
        }

        self['meta'] = {
            'business_tx_id': business_tx_id,
            'task_id': task_id,
            'status': POLICY_STATUS_PENDING,
            'created_at': LocalizedTimeStamp.now_utc().isoformat()
        }
        
        if not sow_window or not sow_window['sow_date']:
            return

        sow_day = sow_window['sow_date']
        self._update_crop_stages(sow_day)

        self['meta']['status'] = POLICY_STATUS_ACTIVE
        self['meta']['created_at'] = LocalizedTimeStamp.now_utc().isoformat()


    @staticmethod   
    def from_dict(new_data):
        group_policy = GroupPolicy()

        for k, v in new_data.items():
            group_policy[k] = v
        
        return group_policy


    def _populate_crop_stages(self):
        template = self['template']
        configs = self._get_crop_stage_configs(template)
        location = template['location']
        crop_stages = []

        crop_stages.append(CropStage(configs[COVERAGE_GERMINATION_DRY], location))
        crop_stages.append(CropStage(configs[COVERAGE_GERMINATION_WET], location))
        crop_stages.append(CropStage(configs[COVERAGE_VEGETATION], location))
        crop_stages.append(CropStage(configs[COVERAGE_FLOWERING], location))
        crop_stages.append(CropStage(configs[COVERAGE_EXCESS_RAIN], location))

        return crop_stages


    def _update_crop_stages(self, sow_date):
        begin_min = 1000000
        end_max = 0

        for stage in self['crop_stages']:
            stage.set_sow_date(sow_date)
            stage_begin = LocalDate.isoformat_to_ordinal(stage['begin_date'])
            stage_end = LocalDate.isoformat_to_ordinal(stage['end_date'])
            
            begin_min = min(stage_begin, begin_min)
            end_max = max(stage_end, end_max)

        self['begin_date'] = LocalDate.ordinal_to_isoformat(begin_min)
        self['end_date'] = LocalDate.ordinal_to_isoformat(end_max)


    def _get_crop_stage_configs(self, template):
        configs = {}
        attr_subset = [
            'name',
            'days_after_start',
            'days_duration',
            'blocks',
            'block_window_length',
            'block_window_overlap',
            'payout_percentage',
            'max_percentage_missing',
            'outlier_active',
            'outlier_value',
            'trigger_active',
            'trigger_type',
            'trigger_value',
            'tick_active',
            'tick_value'
        ]

        for config in template['crop_stage_configurations']:
            key = config['name']
            config_subset = {}

            for attr, value in config.items():
                if attr in attr_subset:
                    config_subset[attr] = value

            configs[key] = config_subset

        return configs

    def _get_deductible(self):
        template = self['template']
        deductible_type = template['deductible_type']
        hurdle = template['hurdle']

        if deductible_type == 2:
            return hurdle

        return 0.0

    def _get_hurdle(self):
        template = self['template']
        hurdle = template['hurdle']

        return hurdle
    

    def to_schema(self):
        crop_stages = []

        for stage_data in self['crop_stages']:
            begin_date = stage_data['begin_date']
            end_date = stage_data['end_date']
            stage_config = stage_data['stage_config']

            crop_stages.append({
                'name': stage_data['name'],
                'location': stage_data['location'],
                'weight': stage_config['payout_percentage'],
                'begin_date': LocalDate.to_isoformat(begin_date),
                'end_date': LocalDate.to_isoformat(end_date),
                'days': stage_config['days_duration'],
                'blocks': stage_config['blocks'],
                'block_length': stage_config['block_window_length'],
                'block_step': stage_config['block_window_overlap'],
                'stage_config': stage_config,
                'stage_blocks': stage_data['stage_blocks'],
                'stage_info': stage_data['stage_info'],
                'loss_blocks': stage_data['loss_blocks'],
                'payout': stage_data['payout'],
                'status': stage_data['status'] 
            })

        obj = {
            Entity.MONGODB_ID: self[Entity.MONGODB_ID],
            'id': self['id'],
            'season': self['season'],
            'crop': self['crop'],
            'activation_window': self['activation_window'],
            'location': self._id_to_location(self['id']),
            'sow_window': self['sow_window'],
            'begin_date': self['begin_date'],
            'end_date': self['end_date'],
            'crop_stages': crop_stages,
            'payout': self['payout'],
            'meta': self['meta'],
        }

        return validate_object(obj, GroupPolicySchema)


    def _id_to_location(self, id):
        pixel = id.split('.')[-1]
        (lat, lng) = pixel_to_latitude_longitude(pixel)

        return {
            'name': pixel,
            'latitude': lat,
            'longitude': lng,
        }


class SowWindow(Entity):

    def __init__(self, sow_window_configuration, sow_window, sow_date):
        self['config'] = sow_window_configuration
        self['window'] = sow_window
        self['sow_date'] = sow_date


# TODO refactor into separate module
class CropStage(Entity):

    def __init__(self, *args):
        super().__init__()

        # default
        if len(args) == 2:
            config = args[0]
            location = args[1]
        
        # should only be called by method from_dict
        elif len(args) == 0:
            return

        # should never happen
        else:
            logging.error("unsupported list for GroupPolicy constructor {}".format(args))
            return
        
        days = config['days_duration']

        self['name'] =  config['name']
        self['location'] =  location
        self['begin_date'] = None
        self['end_date'] = None

        self['blocks'] =  config['blocks']
        self['loss_blocks'] =  0
        self['payout'] =  0.0

        self['stage_config'] = config
        self['stage_blocks'] = []
        self['stage_info'] = []

        self['status'] = STAGE_STATUS_PENDING


    @staticmethod   
    def from_dict(new_data):
        stage = CropStage()

        for k, v in new_data.items():
            stage[k] = v
        
        return stage


    def set_sow_date(self, sow_date):
        config = self['stage_config']
        sow_day = LocalDate().isoformat_to_ordinal(sow_date)

        stage_begin = sow_day + config['days_after_start']
        stage_end = stage_begin + config['days_duration'] - 1

        self['begin_date'] = LocalDate.ordinal_to_isoformat(stage_begin)
        self['end_date'] = LocalDate.ordinal_to_isoformat(stage_end)
        self['status'] = STAGE_STATUS_SCHEDULED

class GroupPolicyException(Exception):

    def __init__(self, message):
        self.err = message
        super().__init__(self.err)
