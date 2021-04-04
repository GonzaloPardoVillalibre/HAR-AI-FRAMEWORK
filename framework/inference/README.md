-----------------------------------------

# Inference environment
This environment exposes a [REST API](https://www.seobility.net/en/wiki/REST_API) that can perform predictions based on an already trained neural network. This API is focused on the ***human classification problem*** and, therefore, the input format must be congruent with the dataset used to train the selected neural network model.

In this way, time series movement windows will be accepted. This windows/tables (**sent int `csv` format**) must contain the exact number of sensors used in the training phase and must also have the same number of time-steps.

As previously mentioned, the 2D-FFT will be commonly used in the training phase; thus, this API will also calculete de 2D-FFT, if that were the case, and apply it to the received image following [the same rule](../pre-processing/doc/images/2DFFT.png).

Similar to the rest of the framework this environment has been designed to server the functionallity over a `JSON configuration file` and its configuration is the key to use the API correctly.

For the reference, this document includes the following sections:
- Data structure.
- Infernce configuration file.
- Usage guide.
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
Contains all the **already trained** neural networks. Each neural network must be stored in a subfolder named with an ***unique identifier***. This identifier will serve the developer to select which neural network is the API exposing. 

Each neural network must have at least:

- Its model stored in a `JSON` format and named as follows `model.json`.
- The weights values stored in another file named as follows `best_weights`.

### config.json
Configuration JSON file.

Some **neural network examples** can be found here:
- ![N2-350-28-9-1](neuralNetworks/N2-350-28-9-1)
- ![N5-350-28-9-1](neuralNetworks/N5-350-28-9-1)

## Infernce configuration file
This configuration file is divided in blocks depending on the deployment environment; this value can be set via the `$ENV` variable. Each environment must contain the following parameters:

| Field | Type | Description |
| -------- |--------- | ----------- |
| neural-network  | String | Selected neural network model from `framework/inference/neuralNetworks`|
| info.movementsList  | `Array<String>`| List of movements supported by the server NN |
| info.sensorsList  | `Array<String>`| List of sensors supported by the server NN |
| rows  | Int | Input rows supported by the server NN |
| columns  | Int | Input columns supported by the server NN (without FFT) |
| channels  | Int | Input channels supported by the server NN |
| FFT | Boolean | Value to force the server to append the FFT for every inference request |

You can find one example ![here](config.json)

## Usage guide
The following operations are supported by the backend:
```sh
# Get service status
curl localhost:8082/api/status
# Reply: {"code":"SUCCESS","message":"Server is online"}

# Get service config
curl localhost:8082/api/config
# Reply: {"info":{"FFT":true,"channels":1,"columns":28,"movementsList":["FigureofEight","HighKneeJog","Jog","JumpingJacks","SpeedSkater","Static","Zigzag","Walk"],"rows":250,"sensorslist":["qRPV","qRTH","qRSK","qRFT","qLTH","qLSK","qLFT"]},"nueral-network":"N2-350-28-9-1"}

# Request inference
curl --location --request POST 'localhost:8082/api/inference' --form 'data_file=@"SOMEWHERE/S10-Zigzag-Orientationjoints-2-103.csv-0"'
# Reply: {"code":"SUCCESS","message":"The performed movement is: Zigzag"}
```

## Production deployment strategy
[TO DO]