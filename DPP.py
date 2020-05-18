# import yaml
import sys
from ruamel.yaml import YAML

pipeline_nodes = []
host_names = []
connection_names = []
nodes_to_change = []


def dump_yaml_file(cntnt, file_name):
    yaml_file = open(file_name, "w")
    yaml.dump(cntnt, yaml_file)
    yaml_file.close()


## get host name
## Assumption: only one hostname in the requirement list.


# gets the list of nodes that has "radon.nodes.nifi.nifipipeline" "type" in it
def get_pipeline_nodes(node_types):
    for nodeName in cntnt["topology_template"]["node_templates"].keys():
        node = cntnt["topology_template"]["node_templates"][nodeName]
        if "type" in node.keys():
            if node["type"] in node_types:
                pipeline_nodes.append(nodeName)


# gets the list of host and connectToPipeline details
def get_host_connection_nodes():
    host_flag = 0
    for pipeline_node in pipeline_nodes:
        node = cntnt["topology_template"]["node_templates"][pipeline_node]["requirements"]
        for n in range(len(node)):
            for key, val in node[n].items():
                if key == "host" and host_flag == 0:
                    host_names.append(val)
                    host_flag = 1
                elif "connect" in key:
                    connection_names.append(val)
                    host_flag = 0
                elif key == "host" and host_flag == 1:
                    connection_names.append('no')
                    host_names.append(val)
                    host_flag = 0


# check the nodes and make a list of nodes where changes have to be done
def get_nodelist_to_edit():
    for connect in range(len(connection_names)):
        # print(pipeline_nodes[connect])
        if (connection_names[connect] != 'no'):
            connection = connection_names[connect]
            pipeline = pipeline_nodes.index(connection)
            connection_host = host_names[pipeline]
            node_host = host_names[connect]
            if (connection_host != node_host):
                nodes_to_change.append(pipeline_nodes[connect])


# defines the function to make changes in the file at required nodes
def make_changes():
    for nodes_change in nodes_to_change:
        node = cntnt["topology_template"]["node_templates"][nodes_change]
        if "requirements" in node.keys():
            for req in node["requirements"]:
                if "connectToPipeline" in req:
                    req["connectToRemotePipeline"] = req["connectToPipeline"]
                    del req["connectToPipeline"]



# prepare a temp dict of nodename and host name
if __name__ == "__main__":
    filename = str(sys.argv[1])
    try:
        node_types={
        "radon.nodes.nifi.nifipipeline",
        "radon.nodes.aws.s3bucket",
        "radon.nodes.aws.lambda"}
        if(filename.lower().endswith(('.yaml','yml'))):
            mydoc = open(filename, "r")
            yaml = YAML(typ='safe')
            yaml.default_flow_style = False
            cntnt = yaml.load(mydoc)
            get_pipeline_nodes(node_types)
            get_host_connection_nodes()
            get_nodelist_to_edit()
            make_changes()
            dump_yaml_file(cntnt, filename)

            mydoc.close()
        else:
            print("Invalid File...please enter YAML file name")
    except FileNotFoundError:
        print("File Not Found")
