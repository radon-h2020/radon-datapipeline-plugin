import unittest
from DataPipelineParser import ModifyConnectionType
from FileOperations import FileOperations
from pathlib import Path
import shutil
import filecmp


class FileParser(unittest.TestCase):

    def setUp(self):
        self.data_pipeline_parser=ModifyConnectionType()
        self.FileOperations = FileOperations()

    def test_iscsar(self):
        value = self.data_pipeline_parser.convert('DataPipelineExample.csar')
        self.assertTrue('csar' in value)

    def test_node_for_modification_is_present(self,file_name='DataPipelineExample.csar'):
        temp_Dir = './temp_Dir'
        file_operations = FileOperations()
        file_operations.unzip_csar(file_name, temp_Dir)
        entry_file_name = file_operations.read_tosca_meta_file(temp_Dir)
        node_list = self.get_nodes(entry_file_name, temp_Dir)

        yaml, content = file_operations.read_file(Path(temp_Dir, entry_file_name))
        self.get_host_connection_nodes(content, node_list)
        self.get_nodelist_to_edit(node_list)
        shutil.rmtree(temp_Dir)
        self.assertTrue(len(self.nodes_to_change)>0)


    def test_output_input_changes(self,original_file_name='Testing_actual/_definitions/radonblueprintsexamples__DataPipelineExample.tosca',modified_file_name='modified_testing/_definitions/radonblueprintsexamples__DataPipelineExample.tosca'):
        cmp=filecmp.cmp(original_file_name,modified_file_name,shallow=True)
        self.assertFalse(cmp)


