# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.policy import Policy
from openapi_server.models.policy_info_all_of import PolicyInfoAllOf
import re
from openapi_server import util

from openapi_server.models.policy import Policy  # noqa: E501
from openapi_server.models.policy_info_all_of import PolicyInfoAllOf  # noqa: E501
import re  # noqa: E501

class PolicyInfo(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, order_no=None, phone_no=None, funding_end_date=None, status=None, crop=None, location=None, sum_insured=None, begin_date=None, end_date=None):  # noqa: E501
        """PolicyInfo - a model defined in OpenAPI

        :param order_no: The order_no of this PolicyInfo.  # noqa: E501
        :type order_no: str
        :param phone_no: The phone_no of this PolicyInfo.  # noqa: E501
        :type phone_no: str
        :param funding_end_date: The funding_end_date of this PolicyInfo.  # noqa: E501
        :type funding_end_date: str
        :param status: The status of this PolicyInfo.  # noqa: E501
        :type status: str
        :param crop: The crop of this PolicyInfo.  # noqa: E501
        :type crop: str
        :param location: The location of this PolicyInfo.  # noqa: E501
        :type location: str
        :param sum_insured: The sum_insured of this PolicyInfo.  # noqa: E501
        :type sum_insured: float
        :param begin_date: The begin_date of this PolicyInfo.  # noqa: E501
        :type begin_date: str
        :param end_date: The end_date of this PolicyInfo.  # noqa: E501
        :type end_date: str
        """
        self.openapi_types = {
            'order_no': str,
            'phone_no': str,
            'funding_end_date': str,
            'status': str,
            'crop': str,
            'location': str,
            'sum_insured': float,
            'begin_date': str,
            'end_date': str
        }

        self.attribute_map = {
            'order_no': 'order_no',
            'phone_no': 'phone_no',
            'funding_end_date': 'funding_end_date',
            'status': 'status',
            'crop': 'crop',
            'location': 'location',
            'sum_insured': 'sum_insured',
            'begin_date': 'begin_date',
            'end_date': 'end_date'
        }

        self._order_no = order_no
        self._phone_no = phone_no
        self._funding_end_date = funding_end_date
        self._status = status
        self._crop = crop
        self._location = location
        self._sum_insured = sum_insured
        self._begin_date = begin_date
        self._end_date = end_date

    @classmethod
    def from_dict(cls, dikt) -> 'PolicyInfo':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PolicyInfo of this PolicyInfo.  # noqa: E501
        :rtype: PolicyInfo
        """
        return util.deserialize_model(dikt, cls)

    @property
    def order_no(self):
        """Gets the order_no of this PolicyInfo.

        Reference to the order no for this policy  # noqa: E501

        :return: The order_no of this PolicyInfo.
        :rtype: str
        """
        return self._order_no

    @order_no.setter
    def order_no(self, order_no):
        """Sets the order_no of this PolicyInfo.

        Reference to the order no for this policy  # noqa: E501

        :param order_no: The order_no of this PolicyInfo.
        :type order_no: str
        """
        if order_no is not None and len(order_no) > 16:
            raise ValueError("Invalid value for `order_no`, length must be less than or equal to `16`")  # noqa: E501
        if order_no is not None and len(order_no) < 1:
            raise ValueError("Invalid value for `order_no`, length must be greater than or equal to `1`")  # noqa: E501

        self._order_no = order_no

    @property
    def phone_no(self):
        """Gets the phone_no of this PolicyInfo.

        Phone number  # noqa: E501

        :return: The phone_no of this PolicyInfo.
        :rtype: str
        """
        return self._phone_no

    @phone_no.setter
    def phone_no(self, phone_no):
        """Sets the phone_no of this PolicyInfo.

        Phone number  # noqa: E501

        :param phone_no: The phone_no of this PolicyInfo.
        :type phone_no: str
        """
        if phone_no is not None and not re.search(r'^[0-9]{9,12}$', phone_no):  # noqa: E501
            raise ValueError("Invalid value for `phone_no`, must be a follow pattern or equal to `/^[0-9]{9,12}$/`")  # noqa: E501

        self._phone_no = phone_no

    @property
    def funding_end_date(self):
        """Gets the funding_end_date of this PolicyInfo.

        Last date until which (additional) premium payments are accepted for this policy  # noqa: E501

        :return: The funding_end_date of this PolicyInfo.
        :rtype: str
        """
        return self._funding_end_date

    @funding_end_date.setter
    def funding_end_date(self, funding_end_date):
        """Sets the funding_end_date of this PolicyInfo.

        Last date until which (additional) premium payments are accepted for this policy  # noqa: E501

        :param funding_end_date: The funding_end_date of this PolicyInfo.
        :type funding_end_date: str
        """
        if funding_end_date is not None and not re.search(r'^20[0-9]{6}$', funding_end_date):  # noqa: E501
            raise ValueError("Invalid value for `funding_end_date`, must be a follow pattern or equal to `/^20[0-9]{6}$/`")  # noqa: E501

        self._funding_end_date = funding_end_date

    @property
    def status(self):
        """Gets the status of this PolicyInfo.


        :return: The status of this PolicyInfo.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this PolicyInfo.


        :param status: The status of this PolicyInfo.
        :type status: str
        """
        allowed_values = ["Active", "Expired"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def crop(self):
        """Gets the crop of this PolicyInfo.

        Crop (also called value chain)  # noqa: E501

        :return: The crop of this PolicyInfo.
        :rtype: str
        """
        return self._crop

    @crop.setter
    def crop(self, crop):
        """Sets the crop of this PolicyInfo.

        Crop (also called value chain)  # noqa: E501

        :param crop: The crop of this PolicyInfo.
        :type crop: str
        """
        allowed_values = ["Maize", "Sorghum", "Greengrams", "Potato", "SoyBeans", "Wheat"]  # noqa: E501
        if crop not in allowed_values:
            raise ValueError(
                "Invalid value for `crop` ({0}), must be one of {1}"
                .format(crop, allowed_values)
            )

        self._crop = crop

    @property
    def location(self):
        """Gets the location of this PolicyInfo.

        Policy location  # noqa: E501

        :return: The location of this PolicyInfo.
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this PolicyInfo.

        Policy location  # noqa: E501

        :param location: The location of this PolicyInfo.
        :type location: str
        """
        if location is not None and not re.search(r'^Pixel[0-9]{6}$', location):  # noqa: E501
            raise ValueError("Invalid value for `location`, must be a follow pattern or equal to `/^Pixel[0-9]{6}$/`")  # noqa: E501

        self._location = location

    @property
    def sum_insured(self):
        """Gets the sum_insured of this PolicyInfo.

        The sum insured for this policy  # noqa: E501

        :return: The sum_insured of this PolicyInfo.
        :rtype: float
        """
        return self._sum_insured

    @sum_insured.setter
    def sum_insured(self, sum_insured):
        """Sets the sum_insured of this PolicyInfo.

        The sum insured for this policy  # noqa: E501

        :param sum_insured: The sum_insured of this PolicyInfo.
        :type sum_insured: float
        """
        if sum_insured is not None and sum_insured > 1000000.0:  # noqa: E501
            raise ValueError("Invalid value for `sum_insured`, must be a value less than or equal to `1000000.0`")  # noqa: E501
        if sum_insured is not None and sum_insured < 0.0:  # noqa: E501
            raise ValueError("Invalid value for `sum_insured`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._sum_insured = sum_insured

    @property
    def begin_date(self):
        """Gets the begin_date of this PolicyInfo.

        The insurance coverage start date for this policy  # noqa: E501

        :return: The begin_date of this PolicyInfo.
        :rtype: str
        """
        return self._begin_date

    @begin_date.setter
    def begin_date(self, begin_date):
        """Sets the begin_date of this PolicyInfo.

        The insurance coverage start date for this policy  # noqa: E501

        :param begin_date: The begin_date of this PolicyInfo.
        :type begin_date: str
        """
        if begin_date is not None and not re.search(r'^20[0-9]{6}$', begin_date):  # noqa: E501
            raise ValueError("Invalid value for `begin_date`, must be a follow pattern or equal to `/^20[0-9]{6}$/`")  # noqa: E501

        self._begin_date = begin_date

    @property
    def end_date(self):
        """Gets the end_date of this PolicyInfo.

        The insurance coverage end date for this policy  # noqa: E501

        :return: The end_date of this PolicyInfo.
        :rtype: str
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """Sets the end_date of this PolicyInfo.

        The insurance coverage end date for this policy  # noqa: E501

        :param end_date: The end_date of this PolicyInfo.
        :type end_date: str
        """
        if end_date is not None and not re.search(r'^20[0-9]{6}$', end_date):  # noqa: E501
            raise ValueError("Invalid value for `end_date`, must be a follow pattern or equal to `/^20[0-9]{6}$/`")  # noqa: E501

        self._end_date = end_date
