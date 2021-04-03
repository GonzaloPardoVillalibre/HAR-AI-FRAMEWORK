import importlib
import tensorflow as tf
from keras.models import model_from_json
import pandas as pd

bestWeightsPath = '/home/gonzalopardo/prueba/TFG/framework/inference/test/best_weights'
modelPath = '/home/gonzalopardo/prueba/TFG/framework/inference/test/model.json'
# load json and create model
json_file = open(modelPath, 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights(bestWeightsPath)
# load weights into new model
df = pd.read_csv('/home/gonzalopardo/prueba/TFG/framework/inference/test/S01-FigureofEight-Orientationjoints-1-4-0.csv', header=None)
df = df.iloc[1:].astype(dtype='float32')
df = df.values
newDF= df.reshape(1,350,84,1)
test = tf.data.Dataset.from_tensor_slices(df)
esult = model.predict(newDF)
print("End of script")
