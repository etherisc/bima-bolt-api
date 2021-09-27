import connexion
import six

from openapi_server.models.bad_request_response import BadRequestResponse  # noqa: E501
from openapi_server.models.data_set import DataSet  # noqa: E501
from openapi_server.models.data_set_validation import DataSetValidation  # noqa: E501
from openapi_server.models.not_found_response import NotFoundResponse  # noqa: E501
from openapi_server.models.resource_id import ResourceId  # noqa: E501
from openapi_server import util
from server_impl.controllers_impl import SeasonDataController_impl


def seasons_get(tenant, env=None):  # noqa: E501
    """seasons_get

    List season data sets # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param env: The environment name
    :type env: str

    :rtype: List[DataSet]
    """
    return SeasonDataController_impl.seasons_get(tenant, env)


def seasons_post(tenant, env=None, data_set=None):  # noqa: E501
    """seasons_post

    Add a season data set # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param env: The environment name
    :type env: str
    :param data_set: 
    :type data_set: dict | bytes

    :rtype: ResourceId
    """
    if connexion.request.is_json:
        data_set = DataSet.from_dict(connexion.request.get_json())  # noqa: E501
    return SeasonDataController_impl.seasons_post(tenant, env, data_set)


def seasons_season_data_id_get(tenant, season_data_id, env=None):  # noqa: E501
    """seasons_season_data_id_get

    List season data sets # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param season_data_id: The ID of a season data set
    :type season_data_id: str
    :param env: The environment name
    :type env: str

    :rtype: DataSet
    """
    return SeasonDataController_impl.seasons_season_data_id_get(tenant, season_data_id, env)


def seasons_season_data_id_validate_get(tenant, season_data_id, env=None):  # noqa: E501
    """seasons_season_data_id_validate_get

    Checks specified season data against season data requirements # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param season_data_id: The ID of a season data set
    :type season_data_id: str
    :param env: The environment name
    :type env: str

    :rtype: DataSetValidation
    """
    return SeasonDataController_impl.seasons_season_data_id_validate_get(tenant, season_data_id, env)
