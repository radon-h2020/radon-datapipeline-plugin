class ValidateRelationships:
    node_capability = []
    old_relationships = []
    local_key_index = []
    remote_key_index = []

    def get_relationship_indexs(self, content):
        nodes = content["topology_template"]["relationship_templates"]
        for keys, values in nodes.items():
            if 'Local' in keys:
                self.local_key_index.append(keys.split('_')[2])
            if 'Remote' in keys:
                self.remote_key_index.append(keys.split('_')[2])

    def validate_capability_and_relationship_of_remote_node(self, content, nodes_to_change):
        for node in nodes_to_change:
            main_node = node.split('#')
            node_requirement = content["topology_template"]["node_templates"][main_node[0]]["requirements"]
            for n in range(len(node_requirement)):
                self.get_relationship_indexs(content)
                index_num = max(self.remote_key_index) + 1 if self.remote_key_index else 0
                for key, val in node_requirement[n].items():
                    if 'connecttopipelineremote' in key.lower():
                        for key_0, val_0 in val.items():
                            if "capability" in key_0.lower():
                                if val_0.lower() != key.lower():
                                    val[key_0] = val_0.replace('Pipeline', 'PipelineRemote')
                            elif "relationship" in key_0.lower():
                                edit_value = val_0.split('_')
                                updated_value = edit_value[0] + '_' + \
                                                edit_value[1].replace('Local', 'Remote') + '_' + str(index_num)
                                val[key_0] = updated_value
                                self.old_relationships.append(val_0 + '#' + updated_value)
        return content

    def validate_capability_and_relationship_of_local_node(self, content, nodes_to_change):
        for node in nodes_to_change:
            main_node = node.split('#')
            node_requirement = content["topology_template"]["node_templates"][main_node[0]]["requirements"]
            for n in range(len(node_requirement)):
                self.get_relationship_indexs(content)
                index_num = int(max(self.local_key_index)) + 1 if self.local_key_index else 0
                for key, val in node_requirement[n].items():
                    if 'connecttopipeline' == key.lower():
                        for key_0, val_0 in val.items():
                            if "capability" in key_0.lower():
                                if val_0.lower() != key.lower():
                                    val[key_0] = val_0.replace('PipelineRemote', 'Pipeline')
                            elif "relationship" in key_0.lower():
                                edit_value = val_0.split('_')
                                updated_value = edit_value[0] + '_' + \
                                                edit_value[1].replace('Remote', 'Local') + '_' + str(index_num)
                                val[key_0] = updated_value
                                self.old_relationships.append(val_0 + '#' + updated_value)
        return content

    def validate_relationship_templates(self, content):
        nodes = content["topology_template"]["relationship_templates"]
        for relation in self.old_relationships:
            new_old_key=relation.split('#')
            for keys,values in nodes.items():
                if (new_old_key[0] in keys) and ('local' in keys.lower()):
                    nodes[new_old_key[1]]=nodes.pop(keys)
                    for key_0,val_0 in values.items():
                        values[key_0]=val_0.replace('Local', 'Remote')
                elif (new_old_key[0] in keys) and ('remote' in keys.lower()):
                    nodes[new_old_key[1]]=nodes.pop(keys)
                    for key_0,val_0 in values.items():
                        values[key_0]=val_0.replace('Remote', 'Local')
        return content

    def delete_duplicate_node_relationship(self,content,duplicate_node_keys):
        for relation_key in duplicate_node_keys:
            del content["topology_template"]["relationship_templates"][relation_key]
        return content
