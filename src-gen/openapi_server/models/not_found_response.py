# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class NotFoundResponse(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, message=None, object_id=None, object_type=None):  # noqa: E501
        """NotFoundResponse - a model defined in OpenAPI

        :param message: The message of this NotFoundResponse.  # noqa: E501
        :type message: str
        :param object_id: The object_id of this NotFoundResponse.  # noqa: E501
        :type object_id: str
        :param object_type: The object_type of this NotFoundResponse.  # noqa: E501
        :type object_type: str
        """
        self.openapi_types = {
            'message': str,
            'object_id': str,
            'object_type': str
        }

        self.attribute_map = {
            'message': 'message',
            'object_id': 'object_id',
            'object_type': 'object_type'
        }

        self._message = message
        self._object_id = object_id
        self._object_type = object_type

    @classmethod
    def from_dict(cls, dikt) -> 'NotFoundResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The NotFoundResponse of this NotFoundResponse.  # noqa: E501
        :rtype: NotFoundResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def message(self):
        """Gets the message of this NotFoundResponse.

        Error message description  # noqa: E501

        :return: The message of this NotFoundResponse.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this NotFoundResponse.

        Error message description  # noqa: E501

        :param message: The message of this NotFoundResponse.
        :type message: str
        """

        self._message = message

    @property
    def object_id(self):
        """Gets the object_id of this NotFoundResponse.

        Object ID queried  # noqa: E501

        :return: The object_id of this NotFoundResponse.
        :rtype: str
        """
        return self._object_id

    @object_id.setter
    def object_id(self, object_id):
        """Sets the object_id of this NotFoundResponse.

        Object ID queried  # noqa: E501

        :param object_id: The object_id of this NotFoundResponse.
        :type object_id: str
        """

        self._object_id = object_id

    @property
    def object_type(self):
        """Gets the object_type of this NotFoundResponse.

        Object type queried  # noqa: E501

        :return: The object_type of this NotFoundResponse.
        :rtype: str
        """
        return self._object_type

    @object_type.setter
    def object_type(self, object_type):
        """Sets the object_type of this NotFoundResponse.

        Object type queried  # noqa: E501

        :param object_type: The object_type of this NotFoundResponse.
        :type object_type: str
        """

        self._object_type = object_type
