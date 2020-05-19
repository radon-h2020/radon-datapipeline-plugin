# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.data_pipeline import DataPipeline  # noqa: E501
from openapi_server.test import BaseTestCase


class TestConvertController(BaseTestCase):
    """ConvertController integration test stubs"""

    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_submit_datapipeline(self):
        """Test case for submit_datapipeline

        Submit a data pipeline for validation and converting
        """
        data_pipeline = {}
        headers = { 
            'Accept': 'application/octet-stream',
            'Content-Type': 'multipart/form-data',
        }
        response = self.client.open(
            '/RadonDataPipeline/convert',
            method='POST',
            headers=headers,
            data=json.dumps(data_pipeline),
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
