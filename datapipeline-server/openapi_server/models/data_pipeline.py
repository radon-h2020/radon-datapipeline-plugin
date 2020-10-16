# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util

from openapi_server.models.FileOperations import FileOperations
import sys
from pathlib import Path, PurePath
from opera.error import DataError, ParseError
from opera.parser import tosca
from opera.storage import Storage
from ruamel.yaml import YAML
import shutil
import zipfile 


class DataPipeline(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    pipeline_nodes = []
    host_names = []
    connection_names = []
    nodes_to_change = []
    _file = ""
    cntnt = {}


    # gets the list of nodes that has "radon.nodes.nifi.nifipipeline" "type" in it
    @classmethod

    def get_nodes(self, file_name, temp_Dir):
        try:
            entry_file = file_name
            storage = Storage(Path(temp_Dir))
            storage.write(entry_file, "root_file")
            ast = tosca.load(Path(temp_Dir), PurePath(entry_file))
            template = ast.get_template({})
            topology = template.instantiate(storage)

            nodes = topology.nodes
            node_keys = list(nodes.keys())
            node_values = list(nodes.values())
            node_list = []
            for val in range(len(node_values)):
                if len(node_values[val].template.requirements) > 0:
                    temp_node = node_keys[val].split('_')
                    node_list.append(temp_node[0])
            return node_list

        except ParseError as e:
            print("{}: {}".format(e.loc, e))
            return 1
        except DataError as e:
            print(str(e))
            return 1



    # gets the list of host and connectToPipeline details
    @classmethod

    def get_host_connection_nodes(self,content, node_list):
        host_flag = 0
        for node_val in node_list:
            node = content["topology_template"]["node_templates"][node_val]["requirements"]
            for n in range(len(node)):
                for key, val in node[n].items():
                    if key == "host" and host_flag == 0:
                        for key_0, val_0 in val.items():
                            if key_0 == 'node':
                                self.host_names.append(val_0)
                                host_flag = 1
                    elif "connect" in key.lower():
                        for key_0, val_0 in val.items():
                            if key_0 == 'node':
                                self.connection_names.append(val_0)
                                host_flag = 0
                    elif key == "host" and host_flag == 1:
                        for key_0, val_0 in val.items():
                            if key_0 == 'node':
                                self.connection_names.append('no')
                                self.host_names.append(val_0)
                                host_flag = 0


    # check the nodes and make a list of nodes where changes have to be done
    @classmethod
    def get_nodelist_to_edit(self,node_list):
        for connect in range(len(self.connection_names)):
            if self.connection_names[connect] != 'no':
                connection = self.connection_names[connect]
                pipeline = node_list.index(connection)
                connection_host = self.host_names[pipeline]
                node_host = self.host_names[connect]
                if connection_host != node_host:
                    self.nodes_to_change.append(node_list[connect])


    # defines the function to make changes in the file at required nodes
    @classmethod
    def make_changes(self,content):
        for nodes_change in self.nodes_to_change:
            node = content["topology_template"]["node_templates"][nodes_change]
            if "requirements" in node.keys():
                for req in node["requirements"]:
                    if "ConnectToPipeline" in req:
                        req["ConnectToRemotePipeline"] = req["ConnectToPipeline"]
                        del req["ConnectToPipeline"]



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

        
        self.pipeline_nodes = []
        self.host_names = []
        self.connection_names = []
        self.nodes_to_change = []

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

            self.pipeline_nodes = []
            self.host_names = []
            self.connection_names = []
            self.nodes_to_change = []
            temp_Dir = './temp_Dir'
            if 'yaml' in filepth:
            file_operations = FileOperations()
            file_operations.unzip_csar(filepath, temp_Dir)
            entry_file_name = file_operations.read_tosca_meta_file(temp_Dir)
            node_list = self.get_nodes(entry_file_name, temp_Dir)

            yaml, content = file_operations.read_file(Path(temp_Dir, entry_file_name))
            self.get_host_connection_nodes(content, node_list)
            self.get_nodelist_to_edit(node_list)
            self.make_changes(content)
            file_operations.write_file(yaml, content, (Path(temp_Dir, entry_file_name)))
            modified_dir=file_operations.zip_csar(filepath, temp_Dir)
            return modified_dir

