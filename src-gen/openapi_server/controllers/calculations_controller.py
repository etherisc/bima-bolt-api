import connexion
import six

from openapi_server.models.bad_request_response import BadRequestResponse  # noqa: E501
from openapi_server.models.calculation_job import CalculationJob  # noqa: E501
from openapi_server.models.calculation_request import CalculationRequest  # noqa: E501
from openapi_server.models.not_found_response import NotFoundResponse  # noqa: E501
from openapi_server.models.resource_id import ResourceId  # noqa: E501
from openapi_server import util
from server_impl.controllers_impl import CalculationsController_impl


def calculations_get(tenant, env=None):  # noqa: E501
    """calculations_get

    List all policy calculation jobs # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param env: The environment name
    :type env: str

    :rtype: List[CalculationJob]
    """
    return CalculationsController_impl.calculations_get(tenant, env)


def calculations_job_id_get(tenant, job_id, env=None):  # noqa: E501
    """calculations_job_id_get

    Get calculation job metadata # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param job_id: The ID of a policy calculation job
    :type job_id: str
    :param env: The environment name
    :type env: str

    :rtype: CalculationJob
    """
    return CalculationsController_impl.calculations_job_id_get(tenant, job_id, env)


def calculations_post(tenant, env=None, calculation_request=None):  # noqa: E501
    """calculations_post

    Create policies for specified data set and calculate payouts. # noqa: E501

    :param tenant: The tenant name
    :type tenant: str
    :param env: The environment name
    :type env: str
    :param calculation_request: 
    :type calculation_request: dict | bytes

    :rtype: ResourceId
    """
    if connexion.request.is_json:
        calculation_request = CalculationRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return CalculationsController_impl.calculations_post(tenant, env, calculation_request)
