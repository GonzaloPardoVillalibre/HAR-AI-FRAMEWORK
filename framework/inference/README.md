-----------------------------------------

# Inference environment
This environment exposes a [REST API](https://www.seobility.net/en/wiki/REST_API) that can perform predictions based on an already trained neural network model. This API is focused on the ***human classification problem*** and, therefore, the input format must be congruent with the dataset used to train the selected neural network model.

In this way, time series movement windows will be accepted. This tables (**sent int `csv` format**) must contain the exact number of sensors used in the training phase and must also have the same number of time-steps.

As mentioned the 2D FFT will be commonly used in the training phase; thus, this API will also calculete de 2D FFT, if that were the case, and apply it to the received image following [the same rule](../pre-processing/doc/images/2DFFT.png).

Similar to the rest of the framework this environment has been designed to server the functionallity over a `JSON configuration file`.  Therefore its configuration is the key to use the API correctly.

For the reference, this document includes the following sections:
- Data structure
- Usage guide & infernce configuration file.
- Production deployment strategy.

## Data structure
       Inference
        │
        └─── neuralNetworks
        │   
        └─── test
        │           
        └─── config.json
        │   
        └─── inferenceServer.py
        │   
        └─── nnUtils.py

### test
Contains some testing scripts.

### inferenceServer
Main script for the flask API.

### nnUtils
Some python functions to support the flask API.

### neuralNetworks
Contains all the **already trained** neural networks. Each neural network must be stored in a subfolder named with an ***unique identifier***. This identifier will server the developer to select which neural network is the API exposing. 

Each neural network must have at least:

- Its model stored in a `JSON` type and named as follows `model.json`
- The weights values stored in another file and named as follows `best_weights`

### config.json
Configuration JSON file.