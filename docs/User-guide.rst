
In this section, you will see how to design a service template using data pipeline nodes. With the current version of TOSCA based data pipeline node types, user can not create a connection with other non-data pipeline TOSCA nodes. The TOSCA data pipeline nodes can be found in `RADON particle <https://github.com/radon-h2020/radon-particles>`_ GitHub repository.


To illustrate the design process, let consider an use case of synchronising AWS S3 bucket and Google Cloud Storage (GCS) bucket.


Demo Video
***********
Users can user RADON IDE, to design a service template in data pipeline apparoche.
In this example, we will create a service template that syncronises Amazon S3 bucket and Google Cloud Storage (GCS) bucket.

The following video provides a 5-minute demo on how to design the service template using RADON IDE.

.. raw:: html

   <iframe width="560" height="315" src="https://github.com/radon-h2020/radon-datapipeline-plugin/blob/master/docs/images/DP_demo_v2.mp4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Steps:

1. Login to RADON IDE (`How to <https://radon-ide.readthedocs.io/en/latest/#access-to-the-radon-ide>`_)
2. Create and Go to your workspace (`How to <https://radon-ide.readthedocs.io/en/latest/#create-a-radon-workspace>`_)
3. Launch the Graphical modelling tool to create a service template (`How to <https://radon-ide.readthedocs.io/en/latest/#how-to-launch-radon-tools>`_)
4. Create the service template (`How to <https://winery.readthedocs.io/en/latest/user/yml/index.html#modeling-an-application>`_)
5. Go to the topology modeller by clicking on `*Topology Template*
6. Form the *Palette* area, create following node types
    `OpenStack` node which is under `radon.nodes.VM`
    `Nifi` TOSCA node from `radon.nodes.nifi`
    `ConsS3Bucket` TOSCA node from `radon.nodes.datapipeline.source`
    `PubGCS` TOSCA node from `radon.nodes.datapipeline.destination`
7. Host `Nifi` on `OpenStack`.
8. Similarly, host `ConsS3Bucket` and `PubGCS` on `Nifi`
9. Connect `ConsS3Bucket` to `PubGCS`. 
10. Save the service template and close the window.
11. Now, in the `Winery Repository` window, export the service template to IDE and close the window.



