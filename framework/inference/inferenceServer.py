# app.py - a minimal flask api
from flask import Flask, request, jsonify, make_response
import requests, json, jwt, time, sys, os, logging
from flask_restful import Resource, Api
from logging.config import dictConfig
import nnUtils as nn
import io
import csv
import codecs
import numpy as np


# main_path = os.getcwd() + '/TFG'
main_path = '/TFG'
nn_path = main_path + '/framework/inference/neuralNetworks'
config_path = main_path + '/framework/inference/config.json'

# Environment variables
log_level = os.environ.get('LOG_LEVEL') or logging.INFO
server_port = os.environ.get('SERVER_PORT') or 8082
server_env = os.environ.get('ENV') or "LOCAL"
defualt_nn =  os.environ.get('DEFAULT_NN') or "N5-250-28-9-1"
f = open(config_path,)
cfg = json.load(f)
cfg_data = cfg[server_env]["info"]
# Launch server
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app = Flask(__name__)
api = Api(app)
app.logger.setLevel(log_level)

app.logger.info('Launching inference server')

#####################
# Get server status #
#####################
@app.route('/api/status', methods=['GET'])
def get_status():   
    data = {'message': 'Server is online', 'code': 'SUCCESS'}
    return make_response(jsonify(data), 201)

#################################
# Get selected NN configuration #
#################################
@app.route('/api/config', methods=['GET'])
def get_config():
    return make_response(jsonify(cfg[server_env]), 201)

############################
# List all neural networks #
############################
@app.route('/api/listAll', methods=['GET'])
def list_all_neural_networks():   
    _, folders, files = next(os.walk(nn_path))
    return '\n'.join(folders)

############################
# Infer movement from csv #
############################
@app.route('/api/inference', methods=['POST'])
def inference():
    app.logger.info('New image recieved')
    flask_file = request.files['data_file']
    if not flask_file:
        data = {'message': 'Upload a CSV file', 'code': 'FAILED'}
        return make_response(jsonify(data), 404)
    
    data = []
    stream = codecs.iterdecode(flask_file.stream, 'utf-8')
    for row in csv.reader(stream, dialect=csv.excel):
        if row:
            data.append(row)
    del data[0]
    data = np.array(data)
    data = data.astype(np.float)
    data = nn.process_input_data(cfg_data, data, app)
    model = nn.load_nueral_network(app, defualt_nn, nn_path)
    result = model.predict(data)
    index = np.argmax(result)
    predicted_movement =cfg_data["movementsList"][index]
    data = {'message': 'The performed movement is: ' + predicted_movement, 'code': 'SUCCESS'}
    return make_response(jsonify(data), 200)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=server_port)
