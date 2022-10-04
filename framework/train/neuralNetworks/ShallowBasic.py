import tensorflow as tf
import utils.utils as nnUtils
from tensorflow.keras import layers

def load_model(input_rows:int, input_columns:int, channels:int, movements_number:int):

    nnUtils.restrict_to_physcial_gpu()
    nnUtils.set_memory_growth()

    model = tf.keras.Sequential([
        layers.Flatten(input_shape = (input_rows,input_columns,channels)),
        layers.Dense(256),
        #layers.BatchNormalization(axis=1),
        layers.Dense(movements_number, activation="softmax")
    ])

    model.summary()
    model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])

    return model

