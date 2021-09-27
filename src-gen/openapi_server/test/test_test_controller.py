# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.test import BaseTestCase


class TestTestController(BaseTestCase):
    """TestController integration test stubs"""

    def test_test_systemtest_post(self):
        """Test case for test_systemtest_post

        
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/test/systemtest',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
