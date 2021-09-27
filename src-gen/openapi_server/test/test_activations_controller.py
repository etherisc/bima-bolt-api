# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.activation import Activation  # noqa: E501
from openapi_server.models.not_found_response import NotFoundResponse  # noqa: E501
from openapi_server.models.resource_id import ResourceId  # noqa: E501
from openapi_server.test import BaseTestCase


class TestActivationsController(BaseTestCase):
    """ActivationsController integration test stubs"""

    def test_activations_event_id_get(self):
        """Test case for activations_event_id_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/acre-test'/activations/{event_id}'.format(event_id='4ad6f91d-6378-4f52-b817-00cbc85ca39x'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_activations_get(self):
        """Test case for activations_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/acre-test'/activations',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_activations_post(self):
        """Test case for activations_post

        
        """
        activation = {
  "mobile_num" : "254711234567",
  "activation_code" : "568947",
  "amount_premium" : 500.0,
  "latitude" : 0.125583,
  "order_number" : "A100097-0321",
  "call_time" : "2000-01-23T04:56:07.000+00:00",
  "county" : "Meru",
  "id" : "ec7fd246-1b51-4f28-bc09-a7f5bae6e143",
  "ward" : "Mount Kenya Forest",
  "longitude" : 35.1592,
  "value_chain" : "Maize"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/acre-test'/activations',
            method='POST',
            headers=headers,
            data=json.dumps(activation),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
