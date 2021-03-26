class ValidateImports:
    type_of_connections = []
    type_of_imports=[]

    def get_types_of_nodes(self, content, node_val):
        self.type_of_connections.clear()
        for node in node_val:
            nodes = content["topology_template"]["node_templates"][node]["requirements"]
            for n in range(len(nodes)):
                for key, val in nodes[n].items():
                    if 'Remote' in key:
                        self.type_of_connections.append('Remote')
                    if 'connecttopipeline' == key.lower():
                        self.type_of_connections.append('Local')

    def import_items_present(self,nodes):
        self.type_of_imports.clear()
        for number_of_imports in range(len(nodes)):
            for keys, values in nodes[number_of_imports].items():
                if 'Remote' in values:
                    self.type_of_imports.append('Remote')
                elif 'Local' in values:
                    self.type_of_imports.append('Local')


    def Validate_import_files(self, content):
        nodes = content['imports']
        get_index=[]
        self.import_items_present(nodes)
        if ('Local' in self.type_of_connections) and ('Remote' in self.type_of_connections) and \
                ('Local' in self.type_of_imports) and ('Remote' not in self.type_of_imports):
            nodes.append({'file': 'radonrelationshipsdatapipeline__ConnectNifiRemote.tosca',
                          'namespace_prefix': 'radonrelationshipsdatapipeline',
                          'namespace_uri': 'radon.relationships.datapipeline'})
        elif 'Local' in self.type_of_connections and 'Remote' in self.type_of_connections and \
                ('Local' not in self.type_of_imports) and ('Remote' in self.type_of_imports):
            nodes.append({'file': 'radonrelationshipsdatapipeline__ConnectNifiLocal.tosca',
                          'namespace_prefix': 'radonrelationshipsdatapipeline',
                          'namespace_uri': 'radon.relationships.datapipeline'})
        for node in range(len(nodes)):
            for key,value in nodes[node].items():
                if 'Local' in self.type_of_connections and ('Remote' not in self.type_of_connections) \
                        and 'Local' not in self.type_of_imports and 'Remote' in self.type_of_imports and ('remote' in value.lower()):
                    nodes[node][key] = value.replace('Remote', 'Local')
                elif ('Remote' in self.type_of_connections) and ('Local' not in self.type_of_connections) \
                        and ('Remote' not in self.type_of_imports) and ('Local' in self.type_of_imports) and ('local' in value.lower()):
                    nodes[node][key] = value.replace('Local', 'Remote')
                elif ('Remote' in self.type_of_connections) and ('Local' not in self.type_of_connections) and \
                        ('Local' in self.type_of_imports) and ('Remote' in self.type_of_imports) and ('local' in value.lower()):
                    get_index.append(node)
                elif ('Remote' not in self.type_of_connections) and ('Local' in self.type_of_connections) and \
                        ('Local' in self.type_of_imports) and ('Remote' in self.type_of_imports) and ('remote' in value.lower()):
                    get_index.append(node)

        for index in get_index:
            del nodes[index]


