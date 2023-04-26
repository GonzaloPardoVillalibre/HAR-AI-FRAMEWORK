import tensorflow as tf
import utils.utils as nnUtils
from tensorflow.keras import layers

def load_model(input_rows:int, input_columns:int, channels:int, movements_number:int):

    model = tf.keras.Sequential([
        layers.Conv2D(32, activation = "relu", input_shape = (input_rows,input_columns,channels), kernel_size=3,padding='same',strides=1),
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
        #layers.Flatten(),
        #layers.Dense(516, activation = "sigmoid"),
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.25),
        layers.Dense(movements_number, activation="softmax")
    ])

    model.summary()
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
    model.compile(loss = "sparse_categorical_crossentropy", optimizer = optimizer, metrics = ["accuracy"])

    return model

