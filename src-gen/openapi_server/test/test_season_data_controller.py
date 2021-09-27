# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.data_set import DataSet  # noqa: E501
from openapi_server.models.not_found_response import NotFoundResponse  # noqa: E501
from openapi_server.models.resource_id import ResourceId  # noqa: E501
from openapi_server.test import BaseTestCase


class TestSeasonDataController(BaseTestCase):
    """SeasonDataController integration test stubs"""

    def test_seasons_get(self):
        """Test case for seasons_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/acre-test'/seasons',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_seasons_post(self):
        """Test case for seasons_post

        
        """
        data_set = {
  "bucket_name" : "my-first-bucket",
  "id" : "test-small",
  "folder_name" : "bimapima-2020-2-small",
  "site_table_file" : "WB_Project SiteTable.xlsx"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/acre-test'/seasons',
            method='POST',
            headers=headers,
            data=json.dumps(data_set),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_seasons_season_data_id_get(self):
        """Test case for seasons_season_data_id_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/acre-test'/seasons/{season_data_id}'.format(season_data_id='test-small'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
