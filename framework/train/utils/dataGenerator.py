import os, json
import tensorflow as tf 
import numpy as np
import pandas as pd
import csv
# This function load the data from the csv, labels it and generates a tensorflow tf

def tf_data_generator(input_path:str, file_list: list, batch_size: int, movements: list, rows:int, columns:int, ouput_path:str):
    i = 0
    # print("File list length: " + str(len(file_list)))
    np.random.shuffle(file_list)
    while True:
        if (i+1)*batch_size >= len(file_list):  # This loop is used to run the generator indefinitely.
            i = 0
            np.random.shuffle(file_list)
        else:
            file_chunk = file_list[i*batch_size:(i+1)*batch_size]
            # print("\nTotal files in file chunk: " + str(len(file_chunk)))
            # print("File chunks from:" + str(i*batch_size) + " to " + str((i+1)*batch_size))
            data = []
            labels = []
            label_classes = tf.constant(movements)
            a = 0
            # b = 0
            for file in file_chunk:
                temp = pd.read_csv(open(input_path+file,'r')) # Change this line to read any other type of file
                data.append(temp.values.reshape(rows,columns,1)) # Convert column data to matrix like data with one channel
                pieces = file.decode("utf-8").split('/')
                activity = pieces[-1].split('-')[1]
                pattern = tf.constant(activity)  # This line has changed
                matched = False
                for j in range(len(label_classes)):
                    if label_classes[j].numpy() == pattern.numpy(): # Pattern is matched against different label_classes
                        labels.append(j)
                        a = a + 1
                        matched = True
                #     else:
                #         b = b +1
                # if matched != True:
                #     print("Activity not matched: {pattern: " + pattern + " }{pieces: " + pieces + " }")
                # else:
                #     print("Activity matched: {pattern: " + pattern + " }{pieces: " + pieces + " }")
            # print("Total files proccessed:" + str(a))
            # print("Files not matching pattern:" + str(b))
            data = np.asarray(data).reshape(-1,rows,columns,1)
            labels = np.asarray(labels)
            # print(len('\n\n'))
            # print(labels.shape)
            # print(len('\n'))
            if (ouput_path):
                # print(len(labels))
                with open(ouput_path, 'a') as f:
                    wtr = csv.writer(f, delimiter =',')
                    wtr.writerow ([labels], )
                    f.close()
            yield data, labels
            i = i + 1
