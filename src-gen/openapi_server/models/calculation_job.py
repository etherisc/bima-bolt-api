# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class CalculationJob(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, job_id=None, season_data_id=None, request_time=None, completion_time=None, status=None):  # noqa: E501
        """CalculationJob - a model defined in OpenAPI

        :param job_id: The job_id of this CalculationJob.  # noqa: E501
        :type job_id: str
        :param season_data_id: The season_data_id of this CalculationJob.  # noqa: E501
        :type season_data_id: str
        :param request_time: The request_time of this CalculationJob.  # noqa: E501
        :type request_time: datetime
        :param completion_time: The completion_time of this CalculationJob.  # noqa: E501
        :type completion_time: datetime
        :param status: The status of this CalculationJob.  # noqa: E501
        :type status: str
        """
        self.openapi_types = {
            'job_id': str,
            'season_data_id': str,
            'request_time': datetime,
            'completion_time': datetime,
            'status': str
        }

        self.attribute_map = {
            'job_id': 'job_id',
            'season_data_id': 'season_data_id',
            'request_time': 'request_time',
            'completion_time': 'completion_time',
            'status': 'status'
        }

        self._job_id = job_id
        self._season_data_id = season_data_id
        self._request_time = request_time
        self._completion_time = completion_time
        self._status = status

    @classmethod
    def from_dict(cls, dikt) -> 'CalculationJob':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The CalculationJob of this CalculationJob.  # noqa: E501
        :rtype: CalculationJob
        """
        return util.deserialize_model(dikt, cls)

    @property
    def job_id(self):
        """Gets the job_id of this CalculationJob.


        :return: The job_id of this CalculationJob.
        :rtype: str
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id):
        """Sets the job_id of this CalculationJob.


        :param job_id: The job_id of this CalculationJob.
        :type job_id: str
        """
        if job_id is not None and len(job_id) > 36:
            raise ValueError("Invalid value for `job_id`, length must be less than or equal to `36`")  # noqa: E501
        if job_id is not None and len(job_id) < 2:
            raise ValueError("Invalid value for `job_id`, length must be greater than or equal to `2`")  # noqa: E501

        self._job_id = job_id

    @property
    def season_data_id(self):
        """Gets the season_data_id of this CalculationJob.


        :return: The season_data_id of this CalculationJob.
        :rtype: str
        """
        return self._season_data_id

    @season_data_id.setter
    def season_data_id(self, season_data_id):
        """Sets the season_data_id of this CalculationJob.


        :param season_data_id: The season_data_id of this CalculationJob.
        :type season_data_id: str
        """
        if season_data_id is not None and len(season_data_id) > 64:
            raise ValueError("Invalid value for `season_data_id`, length must be less than or equal to `64`")  # noqa: E501
        if season_data_id is not None and len(season_data_id) < 1:
            raise ValueError("Invalid value for `season_data_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._season_data_id = season_data_id

    @property
    def request_time(self):
        """Gets the request_time of this CalculationJob.


        :return: The request_time of this CalculationJob.
        :rtype: datetime
        """
        return self._request_time

    @request_time.setter
    def request_time(self, request_time):
        """Sets the request_time of this CalculationJob.


        :param request_time: The request_time of this CalculationJob.
        :type request_time: datetime
        """

        self._request_time = request_time

    @property
    def completion_time(self):
        """Gets the completion_time of this CalculationJob.


        :return: The completion_time of this CalculationJob.
        :rtype: datetime
        """
        return self._completion_time

    @completion_time.setter
    def completion_time(self, completion_time):
        """Sets the completion_time of this CalculationJob.


        :param completion_time: The completion_time of this CalculationJob.
        :type completion_time: datetime
        """

        self._completion_time = completion_time

    @property
    def status(self):
        """Gets the status of this CalculationJob.


        :return: The status of this CalculationJob.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this CalculationJob.


        :param status: The status of this CalculationJob.
        :type status: str
        """
        allowed_values = ["created", "processing", "completed", "error"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status
