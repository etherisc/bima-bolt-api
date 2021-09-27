import logging
import math

PRODUCT = "BimaPima"

CROP_MAIZE = 'Maize'
CROP_SORGHUM = 'Sorghum'
CROP_GREENGRAMS = 'Greengrams'
CROP_POTATO = 'Potato'
CROP_SOY = 'SoyBeans'
CROP_WHEAT = 'Wheat'

CROPS = [CROP_MAIZE, CROP_SORGHUM, CROP_GREENGRAMS, CROP_POTATO, CROP_SOY, CROP_WHEAT]

ACTIVATION_WINDOW_MIN_VALUE = 1
ACTIVATION_WINDOW_MAX_VALUE = 8

ACTIVATION_WINDOWS = ['1', '2', '3', '4', '5', '6', '7', '8']

COVERAGE_GERMINATION_DRY = 'GerminationDry'
COVERAGE_GERMINATION_WET = 'GerminationWet'
COVERAGE_VEGETATION = 'Vegetation'
COVERAGE_FLOWERING = 'Flowering'
COVERAGE_EXCESS_RAIN = 'ExcessRain'

# union of all entity status sets
META_STATUS_ERROR = "Error"
META_STATUS_PENDING = "Pending"
META_STATUS_SCHEDULED = "Scheduled"
META_STATUS_APPLIED = "Applied"
META_STATUS_UNDERWRITTEN = "Underwritten"
META_STATUS_DECLINED = "Declined"
META_STATUS_ACTIVE = "Active"
META_STATUS_EXPIRED = "Expired"
META_STATUS_COMPLETED = "Completed"
META_STATUS = [META_STATUS_PENDING, META_STATUS_SCHEDULED, META_STATUS_APPLIED, META_STATUS_UNDERWRITTEN, META_STATUS_DECLINED, META_STATUS_ACTIVE, META_STATUS_EXPIRED, META_STATUS_COMPLETED]

STAGE_STATUS_PENDING = META_STATUS_PENDING # before stage begin date can be computed
STAGE_STATUS_SCHEDULED = META_STATUS_SCHEDULED # as soon as stage begin date is set and before necessary rainfall data is avilable
STAGE_STATUS_COMPLETED = META_STATUS_COMPLETED # rainfall data is avilable and loss calculation for stage has completed
STAGE_STATUS = [STAGE_STATUS_PENDING, STAGE_STATUS_SCHEDULED, STAGE_STATUS_COMPLETED]

APPLICATION_STATUS_APPLIED = META_STATUS_APPLIED
APPLICATION_STATUS_UNDERWRITTEN = META_STATUS_UNDERWRITTEN
APPLICATION_STATUS_DECLINED = META_STATUS_DECLINED
APPLICATION_STATUS = [APPLICATION_STATUS_APPLIED, APPLICATION_STATUS_UNDERWRITTEN, APPLICATION_STATUS_DECLINED]

POLICY_STATUS_ERROR = META_STATUS_ERROR # if something goes worng during policy construction
POLICY_STATUS_PENDING = META_STATUS_PENDING # before group and individual policy begin date can be computed
POLICY_STATUS_ACTIVE = META_STATUS_ACTIVE # as soon as group and individual policy begin date is set
POLICY_STATUS_COMPLETED = META_STATUS_COMPLETED # as soon as full loss calculation for group policy has been completed
POLICY_STATUS_EXPIRED = META_STATUS_EXPIRED # when all confirmed claims of individual policy are settled
POLICY_STATUS = [POLICY_STATUS_ERROR, POLICY_STATUS_PENDING, POLICY_STATUS_ACTIVE, POLICY_STATUS_COMPLETED, POLICY_STATUS_EXPIRED]

# JSON schema patterns
PROCESS_ID_PATTERN = "^[a-zA-Z0-9/\-\+_.\:]*$" 
ORDER_NO_PATTERN = "^[a-zA-Z0-9/\-\+_.\:]{1,64}$" # TODO should match with order_number openapi spec (len=16) however, need more for system testing
PHONE_NO_PATTERN = "^[0-9]{9,15}$"
SEASON_PATTERN = "^[LS]R20[0-9]{2}$"
LOCATION_PATTERN = "^Pixel[0-9]{6}$"

# TODO needs to be fixed, value should come from voucher not from constant factor
MAX_PAYOUT_FACTOR = 10.0

# TODO needs to be fixed, value should come from site table not from constant factor
HURDLE_MAX_VALUE = 0.15

POSITION_DEDUCTIBLE = "Deductible"
POSITION_GERMINATION_DRY = COVERAGE_GERMINATION_DRY
POSITION_GERMINATION_WET = COVERAGE_GERMINATION_WET
POSITION_VEGETATION = COVERAGE_VEGETATION
POSITION_FLOWERING = COVERAGE_FLOWERING
POSITION_EXCESS_RAIN = COVERAGE_EXCESS_RAIN
POSITION_ITEMS = [POSITION_DEDUCTIBLE, POSITION_GERMINATION_DRY, POSITION_GERMINATION_WET, COVERAGE_VEGETATION, COVERAGE_FLOWERING, COVERAGE_EXCESS_RAIN]

POSITION_NO = {
    POSITION_DEDUCTIBLE : "0",
    POSITION_GERMINATION_DRY : "1",
    POSITION_GERMINATION_WET : "2",
    POSITION_VEGETATION : "3",
    POSITION_FLOWERING : "4",
    POSITION_EXCESS_RAIN : "5"
}

POSITION_STATUS_PENDING = "Pending"
POSITION_STATUS_CONFIRMED = "Confirmed"
POSITION_STATUS_INVALID = "Invalid"
POSITION_STATUS_PAID = "PaidOut"
POSITION_STATUS = [POSITION_STATUS_PENDING, POSITION_STATUS_CONFIRMED, POSITION_STATUS_INVALID, POSITION_STATUS_PAID]

logging.getLogger(__name__).addHandler(logging.NullHandler())

def crop_is_valid(crop):
    if crop not in CROPS:
        logging.error("unknown crop '{}'. known cropse: {}".format(crop, CROPS))
        return False

    return True


def activation_window_is_valid(activation_window):
    try:
        window = int(activation_window)

        if window < ACTIVATION_WINDOW_MIN_VALUE:
            logging.error("activation window value {} too small. valid range is [{}..{}]".format(window, ACTIVATION_WINDOW_MIN_VALUE, ACTIVATION_WINDOW_MAX_VALUE))
            return False
        
        if window > ACTIVATION_WINDOW_MAX_VALUE:
            logging.error("activation window value {} too big. valid range is [{}..{}]".format(window, ACTIVATION_WINDOW_MIN_VALUE, ACTIVATION_WINDOW_MAX_VALUE))
            return False

        return True

    except:
        logging.error("invalid activation window '{}'. conversion to int failed".format(activation_window))
        return False


def get_crop_and_activation_window(crop_activation):
    for crop in CROPS:
        if crop_activation.startswith(crop):
            activation = int(crop_activation[len(crop):])

            if activation_window_is_valid(activation):
                return (crop, str(activation))
    
    logging.warning("failed to parse crop and activation window from '{}'".format(crop_activation))
    return (None, None)
