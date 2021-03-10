-----------------------------------------
# Archive-ics dataset tunning script example 

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


This example will help the developer to understand how the data must be tuned in order to feed the framework correctly. The already mentioned dataset (https://archive.ics.uci.edu/ml/datasets/REALDISP+Activity+Recognition+Dataset ) will be used.

Make yourself sure to correctly understand the database after proceeding with the tuning.

* #### framework-input-dataset
    This folder will contain the tuned dataset ready to feed the framework.

* #### original-dataset
    The developer must include here the folder 

* #### tune.py
    This is the script to run if you want to automatically tune the data.

* #### framework-config-example.json
    This is an example of the framework's configuration file. It can be useful to understand how to correctly configure the framework (based on the database) to act as disered.
