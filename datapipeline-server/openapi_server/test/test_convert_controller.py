# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO
import io

from openapi_server.models.data_pipeline import DataPipeline  # noqa: E501
from openapi_server.test import BaseTestCase
from werkzeug.datastructures import FileStorage

#import requests

class TestConvertController(BaseTestCase):
    """ConvertController integration test stubs"""

#    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_submit_datapipeline(self):
        """Test case for submit_datapipeline

        Submit a data pipeline for validation and converting
        """
        data_pipeline = {}

        fp = io.open('../unit-test/DPP_Testing.csar', 'rb', buffering = 0)
        data_pipeline = BytesIO(fp.read())

        print(data_pipeline)

        headers = {
            'Accept': 'application/octet-stream',
            'Content-Type': 'multipart/form-data',
        }

        data = dict(additionalMetadata='additionalMetadata_example',
                    file=(data_pipeline, 'test.csar', 'application/octet-stream'))

        response = self.client.open(
            '/RadonDataPipeline/convert',
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')

        self.assert200(response, "return code was 200")


if __name__ == '__main__':
    unittest.main()
