RADON Datapipeline Methodology
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following figures shows the basic concept of data pipeline. RADON data pipeline provides an environment to build serverless data intensive applications and handle the movement of data between different clouds in an efficient manner. In the process of data movement, RADON Data pipeline allows the users to apply analyticcal operations onto the data taking the help of serverless platform. Such applications can be designed using TOSCA language.
We see *PipelineBlock* as a basic building block of a TOSCA based data

.. image:: images/BasicDPConcept.png

To carryour different tasks, we...

.. image:: images/PipelineBlock-v1.png

The plugin also contains a REST-based interface, using which users can execute the plugin on-demand or include it as a part of a CI/CD process. DataPipeline plugin is publicly available under the `Apache License 2.0 <http://www.apache.org/licenses/>`_ open-source license in GitHub: https://github.com/radon-h2020/radon-datapipeline-plugin 

The following video provides a 5-minute demo.

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/_6zTEj2ZJ54" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
   
