import unittest
from DataPipelineParser import ModifyConnectionType
from file_operations import FileOperations
from data_encryption import DataEncryption
from validate_imports import ValidateImports
from validate_relationships import ValidateRelationships
from validate_connection_type import ValidateConnectionType
from pathlib import Path
import shutil
import filecmp


class FileParser(unittest.TestCase):

    def setUp(self):
        self.data_pipeline_parser=ModifyConnectionType()
        self.file_operations = FileOperations()
        self.data_encryption = DataEncryption()
        self.verify_connection_type=ValidateConnectionType()
        self.temp_dir= './temp_Dir'




    def test_encryption_decryption_password_mismatch(self,file_name='DPP_Testing.csar'):
        self.file_operations.unzip_csar(file_name, self.temp_dir)
        entry_file_name = self.file_operations.read_tosca_meta_file(self.temp_dir)
        node_list, node_keys = self.data_pipeline_parser.get_nodes(entry_file_name, self.temp_dir)
        yaml, content = self.file_operations.read_file(Path(self.temp_dir, entry_file_name))
        encrypt_decrypt_nodes = self.data_encryption.get_encrypt_decrypt_nodes(content, node_keys)
        shutil.rmtree(self.temp_dir)
        self.assertTrue(len(encrypt_decrypt_nodes)>0)


    def test_duplicate_connections(self,file_name='DPP_Testing.csar'):
        self.file_operations.unzip_csar(file_name, self.temp_dir)
        entry_file_name = self.file_operations.read_tosca_meta_file(self.temp_dir)
        node_list, node_keys = self.data_pipeline_parser.get_nodes(entry_file_name, self.temp_dir)
        yaml, content = self.file_operations.read_file(Path(self.temp_dir, entry_file_name))

        self.verify_connection_type.get_host_connection_nodes(content, node_list)
        self.verify_connection_type.get_nodelist_to_edit(node_list)
        updated_content,duplicate_node_relationships=self.verify_connection_type.delete_duplicate_connection_node(content)
        shutil.rmtree(self.temp_dir)
        self.assertTrue(len(duplicate_node_relationships)>0)


    def test_wrong_connections(self,file_name='DPP_Testing.csar'):
        self.file_operations.unzip_csar(file_name, self.temp_dir)
        entry_file_name = self.file_operations.read_tosca_meta_file(self.temp_dir)
        node_list, node_keys = self.data_pipeline_parser.get_nodes(entry_file_name, self.temp_dir)
        yaml, content = self.file_operations.read_file(Path(self.temp_dir, entry_file_name))
        self.verify_connection_type.get_host_connection_nodes(content, node_list)
        self.verify_connection_type.get_nodelist_to_edit(node_list)
        updated_content, duplicate_node_relationships = self.verify_connection_type.delete_duplicate_connection_node(content)
        updated_content = self.verify_connection_type.make_changes_remote_nodes(updated_content)
        updated_content = self.verify_connection_type.make_changes_local_nodes(updated_content)
        shutil.rmtree(self.temp_dir)
        self.assertTrue((len(self.verify_connection_type.remote_nodes_to_change)+len(self.verify_connection_type.local_nodes_to_change))>0)







