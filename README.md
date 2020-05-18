# radon-datapipeline-plugin
A plugin to make the TOSCA-based data pipeline service blueprint workable.  

This plugin aims to handle the TOSCA CSAR file, which is generated by RAODN-GMT, to make it executable by the RADON-orchestrator. While doing so, this plugin updates the service blueprint based on the artifacts of the user-created TOSCA nodes. 

## Where is this plugin in RADON-Architecture?
We can realized this plugin in the path of RADON-GMT to RADON Orchestrator. Hence, the input to this plugin is the user-created TOSCA service blueprint (i.e. CSAR file) from RADON-GMT and the output the updated CSAR file to the RADON Orchestrator.

## What is inside?
- This plugin unzip the CSAR file, get the YAML file (the service blueprint).
- Parse the the YAML file and understande the node topolology.
- Make any changes/modification to the YAML file itself, if needed.
- Updates the templates, if needed.
- Zip again all and create the CSAR file.
- Pass the ZIP file to the RADON Orchestrator.


This is the initial version of the Data pipeline plugin. In the proceeding version, the plugin will be improved and will come with lots of features. 


.. more info to come soon, stay tuned!!!


#Acknowledgement
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under Grant Agreement No. 825040 (RADON).