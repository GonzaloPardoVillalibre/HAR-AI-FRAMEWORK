import tensorflow as tf
import utils.utils as nnUtils
from tensorflow.keras import layers
import math


def load_model(input_rows:int, input_columns:int, channels:int, movements_number:int):

    model = tf.keras.Sequential([
        
        layers.Reshape((input_rows, input_columns)), #squeeze channel dimension
        layers.LSTM(units=32, return_sequences=True),
        layers.LSTM(units=32,return_sequences=True),
        layers.Reshape((-1,input_rows, 32)),
        #layers.RepeatVector(movements_number),
        layers.Conv2D(64, activation = "relu", kernel_size=5,padding='same',strides=2),
        layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
        layers.Conv2D(128, activation = "relu", kernel_size=3,padding='same',strides=1),
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Flatten(),
        layers.Dense(movements_number, activation = "softmax")
    ])

    #model.summary()

    model.compile(loss = "sparse_categorical_crossentropy", optimizer = tf.keras.optimizers.Adam(learning_rate=0.001), metrics = ["accuracy"])

    return model