import connexion
import six

from openapi_server.models.arc2_cache import Arc2Cache  # noqa: E501
from openapi_server.models.arc2_rainfall import Arc2Rainfall  # noqa: E501
from openapi_server import util
from server_impl.controllers_impl import Arc2Controller_impl


def arc2_cache_get(tenant, date, days, env=None):  # noqa: E501
    """arc2_cache_get

    Get Arc2 cache status # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param date: Start date for rainfall data in YYYYMMDD format
    :type date: str
    :param days: Number of days for rainfall data
    :type days: 
    :param env: The environment name
    :type env: str

    :rtype: Arc2Cache
    """
    return Arc2Controller_impl.arc2_cache_get(tenant, date, days, env)


def arc2_rainfall_get(tenant, location, date, days, env=None):  # noqa: E501
    """arc2_rainfall_get

    Get historic rainfall data # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param location: Rainfall pixel location
    :type location: str
    :param date: Start date for rainfall data in YYYYMMDD format
    :type date: str
    :param days: Number of days for rainfall data
    :type days: 
    :param env: The environment name
    :type env: str

    :rtype: Arc2Rainfall
    """
    return Arc2Controller_impl.arc2_rainfall_get(tenant, location, date, days, env)
