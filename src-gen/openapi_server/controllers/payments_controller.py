import connexion
import six

from openapi_server.models.bad_request_response import BadRequestResponse  # noqa: E501
from openapi_server.models.not_found_response import NotFoundResponse  # noqa: E501
from openapi_server.models.payment import Payment  # noqa: E501
from openapi_server.models.resource_id import ResourceId  # noqa: E501
from openapi_server import util
from server_impl.controllers_impl import PaymentsController_impl


def payments_event_id_get(tenant, event_id, env=None):  # noqa: E501
    """payments_event_id_get

    Get a single policy payment event # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param event_id: A resource identifier
    :type event_id: 
    :param env: The environment name
    :type env: str

    :rtype: Payment
    """
    return PaymentsController_impl.payments_event_id_get(tenant, event_id, env)


def payments_get(tenant, env=None):  # noqa: E501
    """payments_get

    List all policy payment events so far # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param env: The environment name
    :type env: str

    :rtype: List[Payment]
    """
    return PaymentsController_impl.payments_get(tenant, env)


def payments_post(tenant, env=None, payment=None):  # noqa: E501
    """payments_post

    Create a payment event. Do not include an id attribute when posting payment event data. # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param env: The environment name
    :type env: str
    :param payment: 
    :type payment: dict | bytes

    :rtype: ResourceId
    """
    if connexion.request.is_json:
        payment = Payment.from_dict(connexion.request.get_json())  # noqa: E501
    return PaymentsController_impl.payments_post(tenant, env, payment)
