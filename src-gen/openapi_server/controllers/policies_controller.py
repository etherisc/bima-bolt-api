import connexion
import six

from openapi_server.models.bad_request_response import BadRequestResponse  # noqa: E501
from openapi_server.models.claim import Claim  # noqa: E501
from openapi_server.models.not_found_response import NotFoundResponse  # noqa: E501
from openapi_server.models.policy import Policy  # noqa: E501
from openapi_server.models.policy_info import PolicyInfo  # noqa: E501
from openapi_server import util
from server_impl.controllers_impl import PoliciesController_impl


def policies_get(tenant, env=None, phone_no=None, status=None):  # noqa: E501
    """policies_get

    Policy information # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param env: The environment name
    :type env: str
    :param phone_no: Phone number
    :type phone_no: str
    :param status: Policy status
    :type status: str

    :rtype: List[Policy]
    """
    return PoliciesController_impl.policies_get(tenant, env, phone_no, status)


def policies_order_no_claims_get(tenant, order_no, env=None):  # noqa: E501
    """policies_order_no_claims_get

    Provide claims information # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param order_no: The order number to provide policy information for
    :type order_no: str
    :param env: The environment name
    :type env: str

    :rtype: List[Claim]
    """
    return PoliciesController_impl.policies_order_no_claims_get(tenant, order_no, env)


def policies_order_no_get(tenant, order_no, env=None):  # noqa: E501
    """policies_order_no_get

    Provide policy detail information # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param order_no: The order number to provide policy information for
    :type order_no: str
    :param env: The environment name
    :type env: str

    :rtype: PolicyInfo
    """
    return PoliciesController_impl.policies_order_no_get(tenant, order_no, env)
