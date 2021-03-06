# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class CalculationOrder(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, season_data_id=None):  # noqa: E501
        """CalculationOrder - a model defined in OpenAPI

        :param season_data_id: The season_data_id of this CalculationOrder.  # noqa: E501
        :type season_data_id: str
        """
        self.openapi_types = {
            'season_data_id': str
        }

        self.attribute_map = {
            'season_data_id': 'season_data_id'
        }

        self._season_data_id = season_data_id

    @classmethod
    def from_dict(cls, dikt) -> 'CalculationOrder':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The CalculationOrder of this CalculationOrder.  # noqa: E501
        :rtype: CalculationOrder
        """
        return util.deserialize_model(dikt, cls)

    @property
    def season_data_id(self):
        """Gets the season_data_id of this CalculationOrder.


        :return: The season_data_id of this CalculationOrder.
        :rtype: str
        """
        return self._season_data_id

    @season_data_id.setter
    def season_data_id(self, season_data_id):
        """Sets the season_data_id of this CalculationOrder.


        :param season_data_id: The season_data_id of this CalculationOrder.
        :type season_data_id: str
        """
        if season_data_id is not None and len(season_data_id) > 64:
            raise ValueError("Invalid value for `season_data_id`, length must be less than or equal to `64`")  # noqa: E501
        if season_data_id is not None and len(season_data_id) < 1:
            raise ValueError("Invalid value for `season_data_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._season_data_id = season_data_id
