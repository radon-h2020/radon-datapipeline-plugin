# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util

import sys
from pathlib import Path, PurePath
from opera.error import DataError, ParseError
from opera.parser import tosca
from opera.storage import Storage
from ruamel.yaml import YAML
import shutil
import zipfile

from openapi_server.models.file_operations import FileOperations
from openapi_server.models.data_encryption import DataEncryption
from openapi_server.models.validate_imports import ValidateImports
from openapi_server.models.validate_relationships import ValidateRelationships
from openapi_server.models.validate_connection_type import ValidateConnectionType



class DataPipeline(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    _file = ""

    # gets the list of nodes that has "radon.nodes.nifi.nifipipeline" "type" in it
    @classmethod
    def get_nodes(self, file, temp_Dir):
        try:
            entry_file = file
            storage = Storage(Path(temp_Dir))
            storage.write(entry_file, "root_file")
            ast = tosca.load(Path(temp_Dir), PurePath(entry_file))
            template = ast.get_template({})
            topology = template.instantiate(storage)
            nodes = topology.nodes
            node_keys = list(nodes.keys())
            node_values = list(nodes.values())
            node_list = []
            node_keys_updates = []
            for val in range(len(node_values)):
                if len(node_values[val].template.requirements) > 0:
                    temp_node = node_keys[val][:-2]
                    node_list.append(temp_node)
            for node in node_keys:
                node_keys_updates.append(node[:-2])

            return node_list, node_keys_updates

        except ParseError as e:
            print("{}: {}".format(e.loc, e))
            return 1,1
        except DataError as e:
            print(str(e))
            return 1,1



    def __init__(self, file=None):  # noqa: E501
        """DataPipeline - a model defined in OpenAPI

        :param file: The file of this DataPipeline.  # noqa: E501
        :type file: file
        """
        self.openapi_types = {
            'file': file
        }

        self.attribute_map = {
            'file': 'file'
        }


        self._file = file

    @classmethod
    def from_dict(cls, dikt) -> 'DataPipeline':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The DataPipeline of this DataPipeline.  # noqa: E501
        :rtype: DataPipeline
        """
        return util.deserialize_model(dikt, cls)

    @property
    def file(self):
        """Gets the file of this DataPipeline.


        :return: The file of this DataPipeline.
        :rtype: file
        """
        return self._file

    @file.setter
    def file(self, file):
        """Sets the file of this DataPipeline.


        :param file: The file of this DataPipeline.
        :type file: file
        """

        self._file = file
     

    @classmethod
    def convert(self, filepath):

            temp_dir = './temp_Dir'

            file_operations = FileOperations()
            file_operations.unzip_csar(filepath, temp_dir)
            entry_file_name = file_operations.read_tosca_meta_file(temp_dir)
            node_list, node_keys = self.get_nodes(entry_file_name, temp_dir)
            yaml, content = file_operations.read_file(Path(temp_dir, entry_file_name))
            updated_content = self.operation_connectTo(content, node_keys, node_list)
            updated_content = self.operation_encryption(updated_content, node_keys)
            file_operations.write_file(yaml, updated_content, (Path(temp_dir, entry_file_name)))
            modified = file_operations.zip_csar(filepath, temp_dir)
            return modified

    @classmethod
    def operation_connectTo(self, content, node_keys, node_list):
        verify_connection_type=ValidateConnectionType()
        verify_relationships_capabilities=ValidateRelationships()
        verify_imports=ValidateImports()
        verify_connection_type.get_host_connection_nodes(content, node_list)
        verify_connection_type.get_nodelist_to_edit(node_list)
        updated_content,duplicate_node_relationships=verify_connection_type.delete_duplicate_connection_node(content)
        updated_content = verify_relationships_capabilities.delete_duplicate_node_relationship(updated_content,duplicate_node_relationships)
        updated_content = verify_connection_type.make_changes_remote_nodes(updated_content)
        updated_content=verify_connection_type.make_changes_local_nodes(updated_content)
        updated_content = verify_relationships_capabilities.validate_capability_and_relationship_of_remote_node(updated_content,verify_connection_type.remote_nodes_to_change)
        updated_content=verify_relationships_capabilities.validate_capability_and_relationship_of_local_node(updated_content,verify_connection_type.local_nodes_to_change)
        updated_content = verify_relationships_capabilities.validate_relationship_templates(updated_content)
        verify_imports.get_types_of_nodes(updated_content,node_list)
        verify_imports.Validate_import_files(updated_content)
        return updated_content


    @classmethod
    def operation_encryption(self, content, node_keys):
        data_encryption = DataEncryption()
        encrypt_decrypt_nodes = data_encryption.get_encrypt_decrypt_nodes(content, node_keys)
        updated_content = data_encryption.update_password(content, encrypt_decrypt_nodes)
        return updated_content

