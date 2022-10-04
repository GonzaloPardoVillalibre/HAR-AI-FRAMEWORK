import tensorflow as tf
import utils.utils as nnUtils
from tensorflow.keras import layers

def load_model(input_rows:int, input_columns:int, channels:int, movements_number:int):

    

    model = tf.keras.Sequential([
        layers.Flatten(input_shape = (input_rows,input_columns,channels)),
        layers.Dense(256, activation="relu"),
        #layers.Dropout(rate=0.2),
        layers.Dense(128, activation="relu"),
        #layers.Dropout(rate=0.2),
        layers.Dense(64, activation="relu"),
        #layers.Dropout(rate=0.2),
        layers.Dense(32, activation="relu"),
        layers.Dense(movements_number, activation="softmax")
    ])

    model.summary()
    model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])

    return model

