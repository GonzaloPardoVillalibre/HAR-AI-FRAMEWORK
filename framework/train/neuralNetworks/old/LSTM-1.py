import tensorflow as tf
import utils.utils as nnUtils
from tensorflow.keras import layers

def load_model(input_rows:int, input_columns:int, channels:int, movements_number:int):

    model = tf.keras.Sequential([
        # layers.Lambda(lambda x: x[:,:,:,0], input_shape=(*(input_rows,input_columns), 1)), #squeeze channel dimension option 2
        layers.Reshape((input_rows, input_columns)), #squeeze channel dimension
        layers.LSTM(units=256, return_sequences=True),
        layers.Dropout(0.5),
        layers.LSTM(units=128),
        # layers.Dense(256),
        layers.Dense(movements_number, activation = "softmax")
    ])


    model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])
    model.summary()

    return model

# The inputshape for the lstm should be:
# - Samples  --> None
# - Time     --> Rows
# - Features --> Columns
