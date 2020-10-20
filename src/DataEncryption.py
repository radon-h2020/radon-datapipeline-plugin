import random
import string



class DataEncryption():

    def generate_password(self, length=10):
        # below code generates the password
        password_characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(password_characters) for i in range(length))
        return password

    def get_encrypt_decrypt_nodes(self, content, node_list):
        encrypt_password_nodes = []
        decrypt_password_nodes = []
        encrypt_password = []
        encrypt_decrypt_nodes = []
        try:
            for node_val in node_list:
                node = content["topology_template"]["node_templates"][node_val]["type"]
                if 'encrypt' in node.lower():
                    encrypt_password_nodes.append(node_val)

            for encrypt_node in encrypt_password_nodes:
                encrypt_password.append(
                    content["topology_template"]["node_templates"][encrypt_node]["properties"]["password"])

            for encrypt_node in encrypt_password_nodes:
                node_requirements = content["topology_template"]["node_templates"][encrypt_node]["requirements"]
                record_node = encrypt_node
                for node_details in node_requirements:
                    for key, val in node_details.items():
                        if 'connect' in key.lower():
                            for key_node, val_node in val.items():
                                if 'node' in key_node.lower():
                                    record_node = record_node + '*' + val_node
                encrypt_decrypt_nodes.append(record_node)

        except KeyError as ke:
            print('No Properties are found for encrypt and Decrypt nodes')

        return encrypt_decrypt_nodes

    def update_password(self, content, nodes_to_modify):
        for nodes in nodes_to_modify:
            node_list = nodes.split('*')
            updated_password = self.generate_password(10)
            for n in range(0, len(node_list)-1, 1):
                if content["topology_template"]["node_templates"][node_list[n]]["properties"]["password"] != \
                        content["topology_template"]["node_templates"][node_list[n + 1]]["properties"]["password"]:
                    content["topology_template"]["node_templates"][node_list[n]]["properties"][
                        "password"] = updated_password
                    content["topology_template"]["node_templates"][node_list[n + 1]]["properties"][
                        "password"] = updated_password
        return content




