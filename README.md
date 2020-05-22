# radon-datapipeline-plugin
The goal of data pipeline plugin is help solve some of the issues related to designing and orchestrating data pipelines across heterogeneous cloud environments. For example to ensure that data encryption is turned on when data pipeline tasks are deployed across multiple clouds. 

This plugin takes a TOSCA service generated by RADON Graphical Modeling Tool (GMT) as an input (YAML or CSAR file), updates the service blueprint to solve issues (e.g. connectivity, encryption) with the data pipeline templates and generates an updated TOSCA service, which is executable by the RADON Orchestrator.  

## Where is this plugin in RADON-Architecture?
We can realized this plugin in the path of RADON Graphical Modeling Tool to RADON Orchestrator. Hence, the input to this plugin is the user-created TOSCA service blueprint (i.e. CSAR file) from GMT and the output the updated CSAR file to the RADON Orchestrator.

## How does the plugin work?
- This plugin unzip the CSAR file to access the service blueprint (YAML file).
- Parses the the YAML file to understand the node topolology.
- Modifies the service file itself, if needed.
- Updates the templates, if needed.
- Zip again all the files to create the CSAR file.
- Returns the CSAR file, which can then be passed as input to the RADON Orchestrator.

This is the initial version of the Data pipeline plugin. In the proceeding versions, the plugin will be improved with additional features. 

## How to use the plugin as a stand alone tool?
- Download the plugin github repository using git or as a zip file. 
- Make sure that Python environment is working on your machine.
- Keep your TOSCA service ready and note the path. 
- In this version of the Plugin, YAML file is expected as input.
- Execute the following command
```
python DPP_V1 <path to the yaml file>  
```
- Output will be placed in the current directory.

## How to use the plugin API?

Web service version of the plugin is available in the datapipeline-server folder

Download the github project repository 
```bash
git clone https://github.com/radon-h2020/radon-datapipeline-plugin
cd radon-datapipeline-plugin
```

User Docker to build and deploy the data pipeline plugin webservice:
```bash
cd  datapipeline-server

# building the image
docker build -t radon_dpp_server .

# starting up a container
docker run -p 8080:8080 adon_dpp_server
```

Direct your browser to here to access the RadonDataPipeline API ui with REST request example templates:
```
http://localhost:8080/RadonDataPipeline/ui/
```

## Documentation

Online documentation which describes the RADON data pipeline methodology and also provides additional information about the data pipeline plugin is available at https://datapipeline-plugin.readthedocs.io/

## Acknowledgement
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under Grant Agreement No. 825040 (RADON).
