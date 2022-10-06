import tensorflow as tf
import utils.utils as nnUtils
from tensorflow.keras import layers
import math

def load_model(input_rows:int, input_columns:int, channels:int, movements_number:int):

    #callback = tf.keras.callbacks.EarlyStopping(monitor='accuracy',min_delta=0.001, patience=3)#How callbacks work?

    model = tf.keras.Sequential([
        
        layers.Reshape((input_rows, input_columns)), #squeeze channel dimension
        layers.LSTM(units=128, return_sequences=True,activation="tanh"),
        layers.Dropout(0.25),
        layers.LSTM(units=64,return_sequences=True,activation="tanh"),
        layers.Dropout(0.25),
        layers.LSTM(units=32,return_sequences=True,activation="tanh"),
        layers.Dropout(0.25),
        layers.LSTM(units=16,activation="tanh"),
        layers.Dropout(0.25),
        layers.Flatten(),
        layers.Dense(movements_number, activation = "softmax")
    ])

    # model.summary()
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(loss = "sparse_categorical_crossentropy", optimizer = optimizer, metrics = ["accuracy"])

    return model