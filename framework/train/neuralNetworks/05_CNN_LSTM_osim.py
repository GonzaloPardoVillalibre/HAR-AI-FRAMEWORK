import tensorflow as tf
import utils.utils as nnUtils
from tensorflow.keras import layers
import math

def load_model(input_rows:int, input_columns:int, channels:int, movements_number:int):

    lstm_input_rows =  8 #math.ceil(input_rows/16)
    lstm_input_columns = 256 #math.ceil(input_columns/8)

    model = tf.keras.Sequential([
        layers.Conv2D(32, activation = "relu", input_shape = (input_rows,input_columns,channels), kernel_size=3,padding='same'),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.BatchNormalization(axis=1),
        layers.Conv2D(64, activation='relu', kernel_size=3,padding='same'),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.BatchNormalization(axis=1),
        layers.Conv2D(128, activation='relu', kernel_size=3,padding='same'),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.BatchNormalization(axis=1),
        layers.Conv2D(256, activation='relu', kernel_size=3,padding='same'),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.BatchNormalization(axis=1),
        layers.Dropout(0.25),
        #layers.GlobalAveragePooling2D(),
        layers.Reshape((lstm_input_rows,lstm_input_columns)),
        layers.LSTM(units=64, return_sequences=True,activation="tanh"),
        layers.BatchNormalization(),
        layers.Dropout(0.25),
        layers.LSTM(units=32,return_sequences=False),
        layers.BatchNormalization(),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(movements_number, activation="softmax")
    ])

    model.summary()
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(loss = "sparse_categorical_crossentropy", optimizer = optimizer, metrics = ["accuracy"])

    return model

