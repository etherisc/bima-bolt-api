# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.not_found_response import NotFoundResponse  # noqa: E501
from openapi_server.models.payment import Payment  # noqa: E501
from openapi_server.models.resource_id import ResourceId  # noqa: E501
from openapi_server.test import BaseTestCase


class TestPaymentsController(BaseTestCase):
    """PaymentsController integration test stubs"""

    def test_payments_event_id_get(self):
        """Test case for payments_event_id_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/acre-test'/payments/{event_id}'.format(event_id='4ad6f91d-6378-4f52-b817-00cbc85ca39x'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_payments_get(self):
        """Test case for payments_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/acre-test'/payments',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_payments_post(self):
        """Test case for payments_post

        
        """
        payment = {
  "amount_paid" : 50.0,
  "mobile_num" : "254711234567",
  "mpesa_code" : "PC82GDN7C",
  "mpesa_name" : "Jon Doe",
  "order_number" : "A100097-0321",
  "call_time" : "2000-01-23T04:56:07.000+00:00",
  "id" : "8dd6f91d-6378-4f52-b817-00cbc85ca39e"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/acre-test'/payments',
            method='POST',
            headers=headers,
            data=json.dumps(payment),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
