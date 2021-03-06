# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.component import Component
from openapi_server import util

from openapi_server.models.component import Component  # noqa: E501

class Config(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, mongo=None, s3=None, arc2=None, created_at=None):  # noqa: E501
        """Config - a model defined in OpenAPI

        :param mongo: The mongo of this Config.  # noqa: E501
        :type mongo: Component
        :param s3: The s3 of this Config.  # noqa: E501
        :type s3: Component
        :param arc2: The arc2 of this Config.  # noqa: E501
        :type arc2: Component
        :param created_at: The created_at of this Config.  # noqa: E501
        :type created_at: datetime
        """
        self.openapi_types = {
            'mongo': Component,
            's3': Component,
            'arc2': Component,
            'created_at': datetime
        }

        self.attribute_map = {
            'mongo': 'mongo',
            's3': 's3',
            'arc2': 'arc2',
            'created_at': 'created_at'
        }

        self._mongo = mongo
        self._s3 = s3
        self._arc2 = arc2
        self._created_at = created_at

    @classmethod
    def from_dict(cls, dikt) -> 'Config':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Config of this Config.  # noqa: E501
        :rtype: Config
        """
        return util.deserialize_model(dikt, cls)

    @property
    def mongo(self):
        """Gets the mongo of this Config.


        :return: The mongo of this Config.
        :rtype: Component
        """
        return self._mongo

    @mongo.setter
    def mongo(self, mongo):
        """Sets the mongo of this Config.


        :param mongo: The mongo of this Config.
        :type mongo: Component
        """
        if mongo is None:
            raise ValueError("Invalid value for `mongo`, must not be `None`")  # noqa: E501

        self._mongo = mongo

    @property
    def s3(self):
        """Gets the s3 of this Config.


        :return: The s3 of this Config.
        :rtype: Component
        """
        return self._s3

    @s3.setter
    def s3(self, s3):
        """Sets the s3 of this Config.


        :param s3: The s3 of this Config.
        :type s3: Component
        """
        if s3 is None:
            raise ValueError("Invalid value for `s3`, must not be `None`")  # noqa: E501

        self._s3 = s3

    @property
    def arc2(self):
        """Gets the arc2 of this Config.


        :return: The arc2 of this Config.
        :rtype: Component
        """
        return self._arc2

    @arc2.setter
    def arc2(self, arc2):
        """Sets the arc2 of this Config.


        :param arc2: The arc2 of this Config.
        :type arc2: Component
        """
        if arc2 is None:
            raise ValueError("Invalid value for `arc2`, must not be `None`")  # noqa: E501

        self._arc2 = arc2

    @property
    def created_at(self):
        """Gets the created_at of this Config.

        Creation timestamp, omit this property for post requests  # noqa: E501

        :return: The created_at of this Config.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Config.

        Creation timestamp, omit this property for post requests  # noqa: E501

        :param created_at: The created_at of this Config.
        :type created_at: datetime
        """

        self._created_at = created_at
