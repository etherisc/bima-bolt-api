import datetime
import logging
import uuid

from base.model import BaseClass, Entity
from entity.constants import crop_is_valid, activation_window_is_valid

from util.timestamp import LocalizedTimeStamp

class GroupPolicyTemplates(BaseClass):

    def __init__(self):
        self.templates = {}

    def add_template(self, template):
        key = template.name

        if key not in self.templates:
            self.templates[key] = template
            return key
        else:
            raise PolicyTemplateException("group policy template '{template}' already defined ".format(template=key))

    # return best matching policy template for given crop, location and time
    def get_policy_template(self, crop, location, date_activation):
        loggin.warning("REFACTORING check if method GroupPolicyTemplates.get_policy_template is really needed")

        best_candidate = None
        fallback_candidate = None

        for template in self.templates.values():
            if crop == template.crop and location == template.location:
                swc = template['sow_window_configuration']
                sd = datetime.datetime.fromordinal(swc.start_day)
                swc_end = sd + datetime.timedelta(days = swc.window_length - 1)
                swc_end_fallback = sd + datetime.timedelta(days = swc.windows * swc.window_length - 1)

                if date_activation >= sd:
                    if date_activation <= swc_end:
                        return template
                    elif date_activation <= swc_end_fallback:
                        fallback_candidate = template
        
        return fallback_candidate


class GroupPolicyTemplate(Entity):

    def __init__(self, product, season, crop, activation_window, location, deductible_type, max_payout, min_payout, hurdle):
        super().__init__()
        
        self["id"] = '.'.join([product, season, crop, str(activation_window), location])
        self["product"] = product
        self["season"] = season
        self["crop"] = crop
        self["activation_window"] = activation_window
        self["location"] = location
        self['sow_window_configuration'] = None

        # TODO decide for remaining members if move to self.data dict is the way to go
        self.crop_stage_configs = {}
        self['deductible_type'] = deductible_type
        self['max_payout'] = max_payout
        self['min_payout'] = min_payout
        self['hurdle'] = hurdle

    def link_sow_window_config(self, sow_window_config):
        logging.debug("linking sow window config: {}".format(sow_window_config))
        self['sow_window_configuration'] = sow_window_config

    def link_crop_stage_config(self, crop_stage_config):
        logging.debug("linking crop stage config: {}".format(crop_stage_config))
        key = crop_stage_config['name']

        if key not in self.crop_stage_configs:
            self.crop_stage_configs[key] = crop_stage_config
        
            # TODO decide for/against switch to json only
            if "crop_stage_configurations" not in self:
                self["crop_stage_configurations"] = []

            self["crop_stage_configurations"].append(crop_stage_config)
        else:
            raise PolicyTemplateException("policy template already has linked '{stage}' crop stage config".format(stage=key))

class SowWindowConfiguration(Entity):

    def __init__(self, template, start_day, window_length, windows, preceding_days, window_rain_check, preceding_rain_check, start_day_type, start_day_trigger, block_window_length, min_rain_amount, min_rain_days):
        self.template_id = template.ID
        self.start_day = self._calculate_start_day(template["season"], start_day)
        self.window_length = window_length
        self.windows = windows
        self.preceding_days = preceding_days
        self.window_rain_check = window_rain_check
        self.preceding_rain_check = preceding_rain_check

        if not start_day_type in [1, 2]:
            raise PolicyTemplateException("invalid start day type {0} for sow window configuration. valid values in [1, 2]".format(start_day_type))
        
        self.start_day_type = start_day_type
        self.start_day_trigger = start_day_trigger
        self.block_window_length = block_window_length
        self.min_rain_amount = min_rain_amount
        self.min_rain_days = min_rain_days

        self['start_day_type'] = start_day_type
        self['start_date'] = datetime.date.fromordinal(self.start_day)
        self['end_date'] = datetime.date.fromordinal(self.start_day + window_length - 1)
        self['length'] = window_length
        self['windows'] = windows
        self['block_window_length'] = block_window_length
        self['preceding_days'] = preceding_days

        self['start_day_trigger'] = start_day_trigger
        self['min_rain_amount'] = min_rain_amount
        self['min_rain_days'] = min_rain_days
        self['window_rain_check'] = window_rain_check
        self['preceding_rain_check'] = preceding_rain_check

    def _calculate_start_day(self, season, day):
        year = int(season[2:])
        year_begin = datetime.date(year, 1, 1).toordinal()
        return year_begin + day - 1


class CropStageConfiguration(Entity):

    TRIGGER_TYPE_MIN = 1
    TRIGGER_TYPE_MAX = 0

    def __init__(self, template_id, name, payout_percentage, days_after_start, days_duration, block_window_length, block_window_overlap, max_percentage_missing, outlier_active, outlier_value, trigger_active, trigger_type, trigger_value, tick_active, tick_value):
        super().__init__()

        self['template_id'] = template_id 
        self['name'] = name
        self['payout_percentage'] = payout_percentage
        self['days_after_start'] = days_after_start
        self['days_duration'] = days_duration
        self['block_window_length'] = block_window_length
        self['block_window_overlap'] = block_window_overlap
        self['max_percentage_missing'] = max_percentage_missing
        self['outlier_active'] = outlier_active
        self['outlier_value'] = outlier_value
        self['trigger_active'] = trigger_active
        self['trigger_type'] = trigger_type
        self['trigger_value'] = trigger_value
        self['tick_active'] = tick_active
        self['tick_value'] = tick_value
        self['blocks'] = self.blocks()
    
    def blocks(self):
        return int((self['days_duration'] - self['block_window_length'] + 1) / self['block_window_overlap'])


class ActivationWindow(Entity):

    def __init__(self, job_id, product, season, crop, window, begin, end, window_size, windows_to_check):
        super().__init__()
        
        if not crop_is_valid(crop) or not activation_window_is_valid(window):
            return

        self[Entity.ID] = "{}.{}.{}.{}".format(product, season, crop, window)
        self['season'] = season
        self['crop'] = crop
        self['window'] = window
        self['begin_date'] = begin.date()
        # TODO validate with acre that the assumption below is correct
        # setting this fixed avoids some copy/paste errors in the site table excel file
        self['end_date'] = begin.date() + datetime.timedelta(days=13)
        self['window_size'] = int(window_size)
        self['end_extended_date'] = end.date()

        self['job_id'] = job_id
        self['created_at'] = LocalizedTimeStamp.now_utc().isoformat()

        # only extend by a single window even if there would be more available (conservative approach)
        if int(windows_to_check) > 1:
            self['end_extended_date'] = (end + datetime.timedelta(days = int(window_size))).date()
    
    @staticmethod
    def compare_date_with_window(activation_date, activation_window):
        # activation date too early for this window -> no match
        if activation_date < Entity.to_date(activation_window['begin_date']):
            return 0
        
        # activation date too late for this window (extended) -> no match
        if activation_date > Entity.to_date(activation_window['end_extended_date']):
            return 0
        
        # activation date after first window, but inside extended window -> match with 2nd prio
        if activation_date > Entity.to_date(activation_window['end_date']):
            return 2

        # good match (this is what we want)
        return 1

        
class PolicyTemplateException(Exception):

    def __init__(self, message):
        self.err = message
        super().__init__(self.err)
