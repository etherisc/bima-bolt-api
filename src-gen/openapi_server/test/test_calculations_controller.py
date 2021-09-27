# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.calculation_job import CalculationJob  # noqa: E501
from openapi_server.models.calculation_order import CalculationOrder  # noqa: E501
from openapi_server.models.not_found_response import NotFoundResponse  # noqa: E501
from openapi_server.models.resource_id import ResourceId  # noqa: E501
from openapi_server.test import BaseTestCase


class TestCalculationsController(BaseTestCase):
    """CalculationsController integration test stubs"""

    def test_calculations_get(self):
        """Test case for calculations_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/acre-test'/calculations',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculations_job_id_get(self):
        """Test case for calculations_job_id_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/acre-test'/calculations/{job_id}'.format(job_id='4ad6f91d-6378-4f52-b817-00cbc85ca39x'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculations_post(self):
        """Test case for calculations_post

        
        """
        calculation_order = {
  "season_data_id" : "test-small"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/acre-test'/calculations',
            method='POST',
            headers=headers,
            data=json.dumps(calculation_order),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
