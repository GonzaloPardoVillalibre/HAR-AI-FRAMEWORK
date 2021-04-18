import importlib
import tensorflow as tf
import numpy as np
from keras.models import model_from_json

ERROR = "Error"

def load_nueral_network(app, name:str, nn_path:str):
    bestWeightsPath = nn_path + '/' + name + '/best_weights'
    weightsPath = nn_path + '/' + name + '/model.h5'
    modelPath = nn_path + '/' + name + '/model.json'
    app.logger.info('Loading neural network with name: ' + name)
    # load json and create model
    json_file = open(modelPath, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(bestWeightsPath)
    # load weights into new model
    return model

def calculate_FFT(data):
  data = data.astype(np.float32)
  fft_data = np.fft.fft2(data).round(7)
  fft_df_real = fft_data.real.astype(np.float32)
  fft_df_imag = fft_data.imag.astype(np.float32)
  return np.concatenate((data, fft_df_real, fft_df_imag), axis=1)

def process_input_data(cfg_data, data, app):
    if cfg_data["FFT"]:
        if len(data[0]) != int(cfg_data["columns"])*3:
            app.logger.info('FFT must be calculated')
            final_data = calculate_FFT(data)
            try:
                final_data = final_data.reshape(1,cfg_data["rows"],cfg_data["columns"]*3,1)
                return final_data
            except:
                return ERROR
        else:
            try:
                final_data = data.reshape(1,cfg_data["rows"],cfg_data["columns"]*3,1)
                return final_data
            except:
                return ERROR
    try:
        final_data = data.reshape(1,cfg_data["rows"],cfg_data["columns"],1)
        return final_data
    except:
        return ERROR
