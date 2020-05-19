import connexion
import six

from openapi_server.models.data_pipeline import DataPipeline  # noqa: E501
from openapi_server import util


def submit_datapipeline(data_pipeline=None):  # noqa: E501
    """Submit a data pipeline for validation and converting

     # noqa: E501

    :param data_pipeline: 
    :type data_pipeline: dict | bytes

    :rtype: file
    """
    if connexion.request.is_json:
        data_pipeline = DataPipeline.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
