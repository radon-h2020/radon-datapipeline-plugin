RADON Datapipeline Methodology
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following figures shows the basic concept of data pipeline. RADON data pipeline provides an environment to build serverless data intensive applications and handle the movement of data between different clouds in an efficient manner. In the process of data movement, RADON Data pipeline allows the users to apply analyticcal operations onto the data taking the help of serverless platform. Such applications can be designed using TOSCA language.
We see *PipelineBlock* as a basic building block of a TOSCA based data intensive appications. 

.. image:: images/BasicDPConcept.png

A *PipelineBlock* can be designed for different pipeline tasks, such as extracting data from a remote database, or from a AWS S3bucket, processing the data by invoking serverless function etc. In RADON data pipeline, the TOSCA pipelines nodes structured in a manner presented in following figure. 

.. image:: images/PipelineBlock-v1.png


Where is data pipeline plugin in RADON-Architecture?
*****************************************************

This consortium will design and develop a set of TOSCA based pipeline nodes that will be available in `radon  particles <https://github.com/radon-h2020/radon-particles>`_ repository. The service template developed using those datapipeline nodes will then be forwarded to the data pipeline plugin which will make sure that the user-designed service template is workablle and the pipelines can be deployed in the required cloud or local environment.

.. image:: images/datapipelinePlugin.png

The above picture presents the interaction of data pipeline plugin with other RADON components. The pipeline plugin can be invoked through a command line interface or through REST-based interface. 

Plugin's responsibilty?
**************************

The pipeline plugin will be responsible for:
* Parsing and reversing the pipeine CSAR
* Attaching the necessary relationship templates in case of multi cloud pipeline deployment.
* Updating the node templates based on the targeted cloud environment.
* Ensuring the data encryption in multi-cloud service deployment


What is inside data pipeline plugin?
*************************************

1. This plugin unzip the CSAR file, get the YAML file (the service blueprint).
2. Parse the the YAML file and understand the node topolology.
3. Make any changes/modification to the YAML file itself, if needed.
4. Updates the templates, if needed.
5. Zip again all and create the CSAR file.
6. Pass the ZIP file to the RADON Orchestrator.


This is the initial version of the Data pipeline plugin. In the proceeding version, the plugin will be improved and will come with lots of features.


The following video provides a 5-minute demo.

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/_6zTEj2ZJ54" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
   
