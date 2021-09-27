# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.bad_request_response import BadRequestResponse  # noqa: E501
from openapi_server.test import BaseTestCase


class TestPoliciesController(BaseTestCase):
    """PoliciesController integration test stubs"""

    def test_policies_get(self):
        """Test case for policies_get

        
        """
        query_string = [('tenant', 'acre'),
                        ('env', 'test'),
                        ('status', 'Active'),
                        ('phone_no', '254711234567')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/policies',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
