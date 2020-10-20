from pathlib import Path, PurePath
from opera.error import DataError, ParseError
from opera.parser import tosca
from opera.storage import Storage
from FileOperations import FileOperations
from DataEncryption import DataEncryption


class ModifyConnectionType():
    host_names = []
    connection_names = []
    nodes_to_change = []

    '''
        By using the get_nodes, we extract the node details using
        opera parser. This function returns the list of nodes that has requirement
        node in it.
        '''

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
            print(node_keys)
            for val in range(len(node_values)):
                if len(node_values[val].template.requirements) > 0:
                    temp_node = node_keys[val][:-2]
                    node_list.append(temp_node)

            for node in node_keys:
                node_keys_updates.append(node[:-2])

            return node_list, node_keys_updates

        except ParseError as e:
            print("{}: {}".format(e.loc, e))
            return 1
        except DataError as e:
            print(str(e))
            return 1

    '''
    get_host_connection_nodes
        param:  content-> content of tosca/yaml file
                node_list-> list of nodes with requirements
        operation: creates host_names and connection_names list 
    '''

    def get_host_connection_nodes(self, content, node_list):
        host_flag = 0
        try:
            for node_val in node_list:
                node = content["topology_template"]["node_templates"][node_val]["requirements"]
                for n in range(len(node)):
                    for key, val in node[n].items():
                        if key == "host" and host_flag == 0:
                            for key_0, val_0 in val.items():
                                if key_0 == 'node':
                                    # print(val_0)
                                    self.host_names.append(val_0)
                                    host_flag = 1
                        elif "connect" in key.lower():
                            for key_0, val_0 in val.items():
                                if key_0 == 'node':
                                    # print(val_0)
                                    self.connection_names.append(val_0)
                                    host_flag = 0
                        elif key == "host" and host_flag == 1:
                            for key_0, val_0 in val.items():
                                if key_0 == 'node':
                                    # print(val_0)
                                    self.connection_names.append('no')
                                    self.host_names.append(val_0)
                                    host_flag = 0
        except KeyError as ke:
            print('Key not found', ke.__str__())

    '''
    get_nodelist_to_edit
        param: node_list-> list of nodes that has requirements
        operation: it checks the node for which ConnectToPipeline needs to be changed
    '''

    def get_nodelist_to_edit(self, node_list):
        for connect in range(len(self.connection_names)):
            if self.connection_names[connect] != 'no':
                connection = self.connection_names[connect]
                pipeline = node_list.index(connection)
                connection_host = self.host_names[pipeline]
                node_host = self.host_names[connect]
                if connection_host != node_host:
                    self.nodes_to_change.append(node_list[connect])

    '''
    make_changes function :
    param: content -> file content from read_file function
    operation: Edit ConnectToPipeline node
    '''

    def make_changes(self, content):
        for nodes_change in self.nodes_to_change:
            node = content["topology_template"]["node_templates"][nodes_change]
            if "requirements" in node.keys():
                for req in node["requirements"]:
                    if "ConnectToPipeline" in req:
                        req["ConnectToRemotePipeline"] = req["ConnectToPipeline"]
                        del req["ConnectToPipeline"]
        return content

    def convert(self, file_name):
        temp_dir = './temp_Dir'
        file_operations = FileOperations()
        file_operations.unzip_csar(file_name, temp_dir)
        entry_file_name = file_operations.read_tosca_meta_file(temp_dir)
        node_list, node_keys = self.get_nodes(entry_file_name, temp_dir)
        yaml, content = file_operations.read_file(Path(temp_dir, entry_file_name))
        updated_content = self.operation_connectTo(content, node_keys, node_list)

        updated_content = self.operaton_encryption(content,node_keys)

        file_operations.write_file(yaml, updated_content, (Path(temp_dir, entry_file_name)))
        modified = file_operations.zip_csar(file_name, temp_dir)
        return modified

    def operation_connectTo(self, content, node_keys, node_list):
        self.get_host_connection_nodes(content, node_list)
        self.get_nodelist_to_edit(node_list)
        updated_content = self.make_changes(content)
        return updated_content

    def operaton_encryption(self, content, node_keys):
        data_encryption = DataEncryption()
        encrypt_decrypt_nodes = data_encryption.get_encrypt_decrypt_nodes(content, node_keys)
        updated_content = data_encryption.update_password(content, encrypt_decrypt_nodes)
        return updated_content

