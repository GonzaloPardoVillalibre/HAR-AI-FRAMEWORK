import tensorflow as tf
import utils.utils as nnUtils
import numpy as np
from tensorflow.keras import layers
import math

def load_model(input_rows:int, input_columns:int, channels:int, movements_number:int):

    nnUtils.restrict_to_physcial_gpu()
    nnUtils.set_memory_growth()

    lstm_input_rows = math.ceil(input_rows/8)
    lstm_input_columns = math.ceil(input_columns/8)

    model = tf.keras.Sequential([
        layers.Conv2D(32, activation = "relu", input_shape = (input_rows,input_columns,channels), kernel_size=3,padding='same',strides=1),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.BatchNormalization(axis=1),
        layers.Conv2D(64, activation='relu', kernel_size=4,padding='same',strides=1),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.BatchNormalization(axis=1),
        layers.Conv2D(128, activation='relu', kernel_size=4,padding='same',strides=1),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.BatchNormalization(axis=1),
        layers.Reshape((lstm_input_rows,lstm_input_columns*128)), #For each feauture(rows) squeeze all neurons
        layers.LSTM(units=256, return_sequences=False),
        layers.Dropout(0.5),
        layers.Flatten(),
        layers.Dense(516, activation = "relu"),                       #This activation function is the change
        layers.Dense(movements_number, activation="softmax")
    ])

    # model.summary()

    model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])

    return model

# Change of the activation function for the first dense layer. Plot twist "goes wrong".