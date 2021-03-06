# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Claim(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, sequence_no=None, name=None, amount=None, status=None):  # noqa: E501
        """Claim - a model defined in OpenAPI

        :param sequence_no: The sequence_no of this Claim.  # noqa: E501
        :type sequence_no: float
        :param name: The name of this Claim.  # noqa: E501
        :type name: str
        :param amount: The amount of this Claim.  # noqa: E501
        :type amount: float
        :param status: The status of this Claim.  # noqa: E501
        :type status: str
        """
        self.openapi_types = {
            'sequence_no': float,
            'name': str,
            'amount': float,
            'status': str
        }

        self.attribute_map = {
            'sequence_no': 'sequence_no',
            'name': 'name',
            'amount': 'amount',
            'status': 'status'
        }

        self._sequence_no = sequence_no
        self._name = name
        self._amount = amount
        self._status = status

    @classmethod
    def from_dict(cls, dikt) -> 'Claim':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Claim of this Claim.  # noqa: E501
        :rtype: Claim
        """
        return util.deserialize_model(dikt, cls)

    @property
    def sequence_no(self):
        """Gets the sequence_no of this Claim.

        Sequence number of claim  # noqa: E501

        :return: The sequence_no of this Claim.
        :rtype: float
        """
        return self._sequence_no

    @sequence_no.setter
    def sequence_no(self, sequence_no):
        """Sets the sequence_no of this Claim.

        Sequence number of claim  # noqa: E501

        :param sequence_no: The sequence_no of this Claim.
        :type sequence_no: float
        """
        if sequence_no is not None and sequence_no > 99:  # noqa: E501
            raise ValueError("Invalid value for `sequence_no`, must be a value less than or equal to `99`")  # noqa: E501
        if sequence_no is not None and sequence_no < 0:  # noqa: E501
            raise ValueError("Invalid value for `sequence_no`, must be a value greater than or equal to `0`")  # noqa: E501

        self._sequence_no = sequence_no

    @property
    def name(self):
        """Gets the name of this Claim.

        Claim name  # noqa: E501

        :return: The name of this Claim.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Claim.

        Claim name  # noqa: E501

        :param name: The name of this Claim.
        :type name: str
        """
        allowed_values = ["Deductible", "GerminationDry", "Vegetation", "Flowering", "ExcessRain"]  # noqa: E501
        if name not in allowed_values:
            raise ValueError(
                "Invalid value for `name` ({0}), must be one of {1}"
                .format(name, allowed_values)
            )

        self._name = name

    @property
    def amount(self):
        """Gets the amount of this Claim.

        Claim amount (negative values for deductibles)  # noqa: E501

        :return: The amount of this Claim.
        :rtype: float
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this Claim.

        Claim amount (negative values for deductibles)  # noqa: E501

        :param amount: The amount of this Claim.
        :type amount: float
        """
        if amount is not None and amount > 1000000.0:  # noqa: E501
            raise ValueError("Invalid value for `amount`, must be a value less than or equal to `1000000.0`")  # noqa: E501
        if amount is not None and amount < -100000.0:  # noqa: E501
            raise ValueError("Invalid value for `amount`, must be a value greater than or equal to `-100000.0`")  # noqa: E501

        self._amount = amount

    @property
    def status(self):
        """Gets the status of this Claim.

        Claim status  # noqa: E501

        :return: The status of this Claim.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Claim.

        Claim status  # noqa: E501

        :param status: The status of this Claim.
        :type status: str
        """
        allowed_values = ["Pending", "Confirmed"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status
