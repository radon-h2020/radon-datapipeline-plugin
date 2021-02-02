class ValidateConnectionType:
    host_names = []
    connection_names = []
    remote_nodes_to_change = []
    local_nodes_to_change = []
    connection_relation = []
    node_relationship = []
    node_capability = []
    duplicate_node_details = []

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
                                    self.host_names.append(val_0)
                                    host_flag = 1
                        elif "connect" in key.lower():
                            for key_0, val_0 in val.items():
                                if key_0 == 'node':
                                    self.connection_names.append(val_0)
                                    self.connection_relation.append(node_val + "#" + val_0 + '#' + key)
                                    host_flag = 0
                                elif "capability" in key_0.lower():
                                    self.node_capability.append(node_val + "#" + val_0)
                                elif "relationship" in key_0.lower():
                                    self.node_relationship.append(node_val + "#" + val_0)
                        elif key == "host" and host_flag == 1:
                            for key_0, val_0 in val.items():
                                if key_0 == 'node':
                                    self.connection_names.append('no')
                                    self.host_names.append(val_0)
                                    host_flag = 0
                                elif "capability" in key_0.lower():
                                    self.node_capability.append(node_val + "#" + val_0)
                                elif "relationship" in key_0.lower():
                                    self.node_relationship.append(node_val + "#" + val_0)
        except KeyError as ke:
            print('Key not found', ke.__str__())

    def get_nodelist_to_edit(self, node_list):
        for connect in self.connection_relation:
            relation = connect.split('#')
            source_node_index = node_list.index(relation[0])
            dest_node_index = node_list.index(relation[1])
            if (self.host_names[source_node_index] != self.host_names[dest_node_index]) \
                    and ('remote' not in relation[2].lower()):
                self.remote_nodes_to_change.append(relation[0] + "#" + relation[1])
            if self.host_names[source_node_index] == self.host_names[dest_node_index] \
                    and 'remote' in relation[2].lower():
                self.local_nodes_to_change.append(relation[0] + "#" + relation[1])


    def duplicate_connection_index(self,content):
        for nodes in self.remote_nodes_to_change:
            split_node_details = nodes.split('#')
            node = content["topology_template"]["node_templates"][split_node_details[0]]
            for req in range(len(node["requirements"])):
                for val in node["requirements"][req].values():
                    if (split_node_details[1] in val.values()) and ("ConnectToPipeline" in node["requirements"][req]) and (nodes+'#'+"ConnectToPipelineRemote") in self.connection_relation:
                        self.duplicate_node_details.append(nodes+'#'+'remote'+'#'+str(req))
                    elif split_node_details[1] in val.values() and "connectToPipeline" in node["requirements"][req] and (nodes+'#'+"connectToPipelineRemote") in self.connection_relation:
                        self.duplicate_node_details.append(nodes+'#'+'remote'+'#'+str(req))
        for nodes in self.local_nodes_to_change:
            split_node_details = nodes.split('#')
            node = content["topology_template"]["node_templates"][split_node_details[0]]
            for req in range(len(node["requirements"])):
                for val in node["requirements"][req].values():
                    if (split_node_details[1] in val.values()) and ("ConnectToPipelineRemote" in node["requirements"][req]) and (nodes+'#'+"ConnectToPipeline") in self.connection_relation:
                        self.duplicate_node_details.append(nodes+'#'+'local'+'#'+str(req))
                    elif split_node_details[1] in val.values() and "connectToPipelineRemote" in node["requirements"][req] and (nodes+'#'+"connectToPipeline") in self.connection_relation:
                        self.duplicate_node_details.append(nodes+'#'+'local'+'#'+str(req))


    def delete_duplicate_connection_node(self,content):
        self.duplicate_connection_index(content)
        duplicate_node_relationships=[]
        for val in self.duplicate_node_details:
            get_index=val.split('#')
            node=content["topology_template"]["node_templates"][get_index[0]]["requirements"][int(get_index[3])]
            for key,val in node.items():
                for key_0,val_0 in val.items():
                    if key_0=='relationship':
                        duplicate_node_relationships.append(val_0)
            del content["topology_template"]["node_templates"][get_index[0]]["requirements"][int(get_index[3])]
            if get_index[2]=='local':
                self.local_nodes_to_change.remove(get_index[0]+"#"+get_index[1])
            elif get_index[2]=='remote':
                self.remote_nodes_to_change.remove(get_index[0]+"#"+get_index[1])
        return content,duplicate_node_relationships




    def make_changes_remote_nodes(self, content):
        for nodes_change in self.remote_nodes_to_change:
            split_node_details = nodes_change.split('#')
            node = content["topology_template"]["node_templates"][split_node_details[0]]
            for req in node["requirements"]:
                for val in req.values():
                    if split_node_details[1] in val.values() and "ConnectToPipeline" in req:
                        req["ConnectToPipelineRemote"] = req["ConnectToPipeline"]
                        del req["ConnectToPipeline"]
                    elif split_node_details[1] in val.values() and "connectToPipeline" in req:
                        req["connectToPipelineRemote"] = req["connectToPipeline"]
                        del req["connectToPipeline"]
        return content

    def make_changes_local_nodes(self, content):
        for nodes_change in self.local_nodes_to_change:
            split_node_details = nodes_change.split('#')
            node = content["topology_template"]["node_templates"][split_node_details[0]]
            for req in node["requirements"]:
                for val in req.values():
                    if split_node_details[1] in val.values() and "ConnectToPipelineRemote" in req:
                        req["ConnectToPipeline"] = req["ConnectToPipelineRemote"]
                        del req["ConnectToPipelineRemote"]
                    elif split_node_details[1] in val.values() and "connectToPipelineRemote" in req:
                        req["connectToPipeline"] = req["connectToPipelineRemote"]
                        del req["connectToPipelineRemote"]
        return content
