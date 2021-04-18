import tensorflow as tf
import utils.utils as nnUtils
from tensorflow.keras import layers

def load_model(input_rows:int, input_columns:int, channels:int, movements_number:int):

    nnUtils.restrict_to_physcial_gpu()
    nnUtils.set_memory_growth()

    input_shape = (1, input_columns, channels)

    model = tf.keras.Sequential([
        layers.Reshape((input_rows,) + input_shape, input_shape=input_shape),
        layers.ConvLSTM2D(filters=8, kernel_size=(3, 3),
                     data_format= 'channels_last',
                     activation='relu',
                     return_sequences=True,
                     padding='same'),
        layers.BatchNormalization(),
        layers.ConvLSTM2D(32, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dropout(0.5),
        layers.Flatten(),
        layers.Dense(movements_number, activation = "softmax")
    ])

    # model.summary()

    model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])

    return model

# The inputshape for the convLSTM2D should be:
# - Samples  --> None
# - Time     --> 352
# - Rows     --> 1
# - Columns  --> 84
# - Channels --> 1

# I have to look to reshape input size (352,84,1) to what I want