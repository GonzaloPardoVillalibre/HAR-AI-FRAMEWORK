import tensorflow as tf
import utils.utils as nnUtils
import numpy as np
from tensorflow.keras import layers
import math

def load_model(input_rows:int, input_columns:int, channels:int, movements_number:int):

    lstm_input_rows = math.ceil(input_rows/4)
    lstm_input_columns = math.ceil(input_columns/4)

    model = tf.keras.Sequential([
        layers.Conv2D(64, activation='relu', kernel_size=4,padding='same',strides=1),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.BatchNormalization(axis=1),
        layers.Dropout(0.2),
        layers.Conv2D(64, activation='relu', kernel_size=4,padding='same',strides=1),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.BatchNormalization(axis=1),
        layers.Dropout(0.2),
        layers.Reshape((lstm_input_rows,lstm_input_columns*64)), #For each feauture(rows) squeeze all neurons
        layers.LSTM(units=512, return_sequences=False),
        layers.Dropout(0.5),
        layers.Flatten(),
        layers.Dense(516, activation = "sigmoid"),
        layers.Dense(movements_number, activation="softmax")
    ])

    # model.summary()

    model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])

    return model

#Try to reduce overfitting from CNN+LSTM-4 by aumenting drop out of last layer.
