import numpy as np
import os
import glob
import tensorflow as tf 
import pandas as pd
from tensorflow.keras import layers

train_files = glob.glob("./vicon/pre-processing/final-dataset/train-set/*")
test_files = glob.glob("./vicon/pre-processing/final-dataset/test-set/*")
validation_files = glob.glob("./vicon/pre-processing/final-dataset/validation-set/*")


def tf_data_generator(file_list, batch_size = 20):
    i = 0
    while True:
        if i*batch_size >= len(file_list):  # This loop is used to run the generator indefinitely.
            i = 0
            np.random.shuffle(file_list)
        else:
            file_chunk = file_list[i*batch_size:(i+1)*batch_size] 
            data = []
            labels = []
            label_classes = tf.constant([
                        "FigureofEight",
                        "HighKneeJog",
                        "JumpingJacks",
                        "SpeedSkater",
                        "Zigzag"
                        ])
            for file in file_chunk:
                temp = pd.read_csv(open(file,'r')) # Change this line to read any other type of file
                temp = temp.drop(temp.columns[0], axis=1)
                data.append(temp.values.reshape(128,28,1)) # Convert column data to matrix like data with one channel
                pieces = file.decode("utf-8").split('/')
                activity = pieces[-1].split('-')[1]
                pattern = tf.constant(activity)  # This line has changed
                for j in range(len(label_classes)):
                    if label_classes[j].numpy() == pattern.numpy(): # Pattern is matched against different label_classes
                        labels.append(j)  
            data = np.asarray(data).reshape(-1,128,28,1)
            labels = np.asarray(labels)
            yield data, labels
            i = i + 1

batch_size = 128
train_dataset = tf.data.Dataset.from_generator(tf_data_generator,args= [train_files, batch_size],output_types = (tf.complex64, tf.float32), output_shapes = ((None,128,28,1),(None,)))
test_dataset = tf.data.Dataset.from_generator(tf_data_generator,args= [test_files, batch_size],output_types = (tf.complex64, tf.float32), output_shapes = ((None,128,28,1),(None,)))
validation_dataset = tf.data.Dataset.from_generator(tf_data_generator,args= [validation_files, batch_size],output_types = (tf.complex64, tf.float32), output_shapes = ((None,128,28,1),(None,)))

model = tf.keras.Sequential([
    layers.Conv2D(16, activation = "relu", input_shape = (128,28,1), kernel_size=3,padding='same',strides=1),
    layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
    layers.BatchNormalization(axis=1),
    layers.Conv2D(32, activation='relu', kernel_size=4,padding='same',strides=1),
    layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
    layers.BatchNormalization(axis=1),
    layers.Conv2D(64, activation='relu', kernel_size=4,padding='same',strides=1),
    layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
    layers.BatchNormalization(axis=1),
    layers.Conv2D(128, activation='relu', kernel_size=4,padding='same',strides=1),
    layers.MaxPooling2D(pool_size=2, strides=2, padding='same'),
    layers.BatchNormalization(axis=1),
    layers.Dropout(0.5),
    layers.Flatten(),
    layers.Dense(6, activation = "softmax")
])

model.summary()

model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])


steps_per_epoch =  50
validation_steps =  5
steps =  25

model.fit(train_dataset, validation_data = validation_dataset, steps_per_epoch = steps_per_epoch,
         validation_steps = validation_steps, epochs = 20)

test_loss, test_accuracy = model.evaluate(test_dataset, steps = 10)

print("Test loss: ", test_loss)
print("Test accuracy:", test_accuracy)
