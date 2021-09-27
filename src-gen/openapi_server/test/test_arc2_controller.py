# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.arc2_cache import Arc2Cache  # noqa: E501
from openapi_server.models.arc2_rainfall import Arc2Rainfall  # noqa: E501
from openapi_server.test import BaseTestCase


class TestArc2Controller(BaseTestCase):
    """Arc2Controller integration test stubs"""

    def test_arc2_cache_get(self):
        """Test case for arc2_cache_get

        
        """
        query_string = [('tenant', 'acre'),
                        ('env', 'test')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/arc2/cache',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_arc2_rainfall_get(self):
        """Test case for arc2_rainfall_get

        
        """
        query_string = [('tenant', 'acre'),
                        ('env', 'test'),
                        ('location', 'Pixel404557'),
                        ('date', '20210330'),
                        ('days', 14)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/arc2/rainfall',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
