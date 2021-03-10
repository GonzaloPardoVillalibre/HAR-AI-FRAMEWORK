-----------------------------------------
# Harvard dataset tunning script example 

## Data structure


       ./
        │
        └─── framework-input-dataset/
        │   
        └─── original-dataset/
        │   
        └─── tune.py
        │   
        └─── framewokr-config-example.json 


This example will help the developer to understand how the data must be tuned in order to feed the framework correctly. The already mentioned dataset (https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/9QDD5J ) will be used.

As this database was the origin of this project a more detailed explanation can be found [here](../../../doc/documents/this-problem.md).

* #### framework-input-dataset
    This folder will contain the tuned dataset ready to feed the framework.

* #### original-dataset
    The developer must include here the folder 

* #### tune.py
    This is the script to run if you want to automatically tune the data.

* #### framework-config-example.json
    This is an example of the framework's configuration file. It can be useful to understand how to correctly configure the framework (based on the database) to act as disered.
