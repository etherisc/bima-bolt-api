import connexion
import six

from openapi_server.models.activation import Activation  # noqa: E501
from openapi_server.models.bad_request_response import BadRequestResponse  # noqa: E501
from openapi_server.models.not_found_response import NotFoundResponse  # noqa: E501
from openapi_server.models.planting_window import PlantingWindow  # noqa: E501
from openapi_server.models.resource_id import ResourceId  # noqa: E501
from openapi_server import util
from server_impl.controllers_impl import ActivationsController_impl


def activations_event_id_get(tenant, event_id, env=None):  # noqa: E501
    """activations_event_id_get

    Get a single policy activation event # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param event_id: A resource identifier
    :type event_id: 
    :param env: The environment name
    :type env: str

    :rtype: Activation
    """
    return ActivationsController_impl.activations_event_id_get(tenant, event_id, env)


def activations_get(tenant, env=None):  # noqa: E501
    """activations_get

    List all policy activation events so far # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param env: The environment name
    :type env: str

    :rtype: List[Activation]
    """
    return ActivationsController_impl.activations_get(tenant, env)


def activations_planting_window_get(tenant, env=None, reference_date=None, crop=None, latitude=None, longitude=None):  # noqa: E501
    """activations_planting_window_get

    Provide the planting window for the current season given crop and location parameters # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param env: The environment name
    :type env: str
    :param reference_date: The reference date for the request
    :type reference_date: str
    :param crop: Crop (also called value chain)
    :type crop: str
    :param latitude: Latitude of the location of the mobile device at the time of the call. Any number between -40 (40 degrees South) to 40 (40 degrees North)
    :type latitude: 
    :param longitude: Longitude of the location of the mobile device at the time of the call. Any number between -20 (20 degrees West) to 55 (55 degrees East)
    :type longitude: 

    :rtype: PlantingWindow
    """
    return ActivationsController_impl.activations_planting_window_get(tenant, env, reference_date, crop, latitude, longitude)


def activations_post(tenant, env=None, activation=None):  # noqa: E501
    """activations_post

    Create a policy activation event. Do not include an id attribute when posting activation event data. # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param env: The environment name
    :type env: str
    :param activation: 
    :type activation: dict | bytes

    :rtype: ResourceId
    """
    if connexion.request.is_json:
        activation = Activation.from_dict(connexion.request.get_json())  # noqa: E501
    return ActivationsController_impl.activations_post(tenant, env, activation)
