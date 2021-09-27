import connexion
import six

from openapi_server.models.config import Config  # noqa: E501
from openapi_server import util
from server_impl.controllers_impl import AdminController_impl


def config_get(tenant, env=None):  # noqa: E501
    """config_get

    Get config for external components # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param env: The environment name
    :type env: str

    :rtype: Config
    """
    return AdminController_impl.config_get(tenant, env)


def config_post(tenant, env=None, config=None):  # noqa: E501
    """config_post

    Set config for external components # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param env: The environment name
    :type env: str
    :param config: 
    :type config: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        config = Config.from_dict(connexion.request.get_json())  # noqa: E501
    return AdminController_impl.config_post(tenant, env, config)
