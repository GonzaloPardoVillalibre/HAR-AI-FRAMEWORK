import tensorflow as tf
from tensorflow import keras
from keras import layers
import utils.utils as nnUtils

def load_model(input_rows:int, input_columns:int, channels:int, movements_number:int):

    model = tf.keras.Sequential([
        layers.Flatten(input_shape = (input_rows,input_columns,channels)),
        layers.Dense(256,activation="relu",kernel_regularizer=tf.keras.regularizers.L2(0.01)),
        #layers.Dropout(rate=0.2),
        layers.Dense(128, activation="relu",kernel_regularizer=tf.keras.regularizers.L2(0.01)),
        #layers.Dropout(rate=0.2),
        layers.Dense(64, activation="relu",kernel_regularizer=tf.keras.regularizers.L2(0.01)),
        #layers.Dropout(rate=0.2),
        layers.Dense(32, activation="relu",kernel_regularizer=tf.keras.regularizers.L2(0.01)),
        layers.Dense(movements_number, activation="softmax")
    ])

    model.summary()
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])

    return model

