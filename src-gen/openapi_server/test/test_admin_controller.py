# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.config import Config  # noqa: E501
from openapi_server.test import BaseTestCase


class TestAdminController(BaseTestCase):
    """AdminController integration test stubs"""

    def test_config_get(self):
        """Test case for config_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/acre-test'/config',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_config_post(self):
        """Test case for config_post

        
        """
        config = {
  "mongo" : {
    "resource" : "demo",
    "port" : 0.8008281904610115,
    "access_secret" : "access_secret",
    "host" : "172.22.251.203",
    "access_id" : "access_id",
    "timeout" : 1000
  },
  "s3" : {
    "resource" : "demo",
    "port" : 0.8008281904610115,
    "access_secret" : "access_secret",
    "host" : "172.22.251.203",
    "access_id" : "access_id",
    "timeout" : 1000
  },
  "created_at" : "2000-01-23T04:56:07.000+00:00"
}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/acre-test'/config',
            method='POST',
            headers=headers,
            data=json.dumps(config),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
