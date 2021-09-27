# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
import re
from openapi_server import util

import re  # noqa: E501

class Arc2Rainfall(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, date_begin=None, date_end=None, days=None, rainfall=None):  # noqa: E501
        """Arc2Rainfall - a model defined in OpenAPI

        :param date_begin: The date_begin of this Arc2Rainfall.  # noqa: E501
        :type date_begin: str
        :param date_end: The date_end of this Arc2Rainfall.  # noqa: E501
        :type date_end: str
        :param days: The days of this Arc2Rainfall.  # noqa: E501
        :type days: float
        :param rainfall: The rainfall of this Arc2Rainfall.  # noqa: E501
        :type rainfall: List[str]
        """
        self.openapi_types = {
            'date_begin': str,
            'date_end': str,
            'days': float,
            'rainfall': List[str]
        }

        self.attribute_map = {
            'date_begin': 'date_begin',
            'date_end': 'date_end',
            'days': 'days',
            'rainfall': 'rainfall'
        }

        self._date_begin = date_begin
        self._date_end = date_end
        self._days = days
        self._rainfall = rainfall

    @classmethod
    def from_dict(cls, dikt) -> 'Arc2Rainfall':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Arc2Rainfall of this Arc2Rainfall.  # noqa: E501
        :rtype: Arc2Rainfall
        """
        return util.deserialize_model(dikt, cls)

    @property
    def date_begin(self):
        """Gets the date_begin of this Arc2Rainfall.

        Rainfall data start date in YYYYMMDD format  # noqa: E501

        :return: The date_begin of this Arc2Rainfall.
        :rtype: str
        """
        return self._date_begin

    @date_begin.setter
    def date_begin(self, date_begin):
        """Sets the date_begin of this Arc2Rainfall.

        Rainfall data start date in YYYYMMDD format  # noqa: E501

        :param date_begin: The date_begin of this Arc2Rainfall.
        :type date_begin: str
        """
        if date_begin is not None and not re.search(r'^20[0-9]{6}$', date_begin):  # noqa: E501
            raise ValueError("Invalid value for `date_begin`, must be a follow pattern or equal to `/^20[0-9]{6}$/`")  # noqa: E501

        self._date_begin = date_begin

    @property
    def date_end(self):
        """Gets the date_end of this Arc2Rainfall.


        :return: The date_end of this Arc2Rainfall.
        :rtype: str
        """
        return self._date_end

    @date_end.setter
    def date_end(self, date_end):
        """Sets the date_end of this Arc2Rainfall.


        :param date_end: The date_end of this Arc2Rainfall.
        :type date_end: str
        """
        if date_end is not None and not re.search(r'^20[0-9]{6}$', date_end):  # noqa: E501
            raise ValueError("Invalid value for `date_end`, must be a follow pattern or equal to `/^20[0-9]{6}$/`")  # noqa: E501

        self._date_end = date_end

    @property
    def days(self):
        """Gets the days of this Arc2Rainfall.

        Rainfall data for number of days  # noqa: E501

        :return: The days of this Arc2Rainfall.
        :rtype: float
        """
        return self._days

    @days.setter
    def days(self, days):
        """Sets the days of this Arc2Rainfall.

        Rainfall data for number of days  # noqa: E501

        :param days: The days of this Arc2Rainfall.
        :type days: float
        """

        self._days = days

    @property
    def rainfall(self):
        """Gets the rainfall of this Arc2Rainfall.

        Rainfall data  # noqa: E501

        :return: The rainfall of this Arc2Rainfall.
        :rtype: List[str]
        """
        return self._rainfall

    @rainfall.setter
    def rainfall(self, rainfall):
        """Sets the rainfall of this Arc2Rainfall.

        Rainfall data  # noqa: E501

        :param rainfall: The rainfall of this Arc2Rainfall.
        :type rainfall: List[str]
        """

        self._rainfall = rainfall