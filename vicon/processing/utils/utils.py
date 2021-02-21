import os, re, json, datetime, random, csv
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
import seaborn as sn
from string import ascii_uppercase

def filter_files_by_regex(files:list, regex:str):
    filtered_list = [val for val in files if re.search(regex, val)]
    return filtered_list

def build_regex_for_subjects(subjects:list):
    user_regex_string ="^("
    for subject in subjects:
        user_regex_string = (user_regex_string + subject + '|')
    user_regex_string = user_regex_string[:-1] + ')'
    user_regex_string = re.compile(user_regex_string)
    return user_regex_string

def build_regex_for_movement(movements:list):
    user_regex_string ="("
    for movement in movements:
        user_regex_string = (user_regex_string + movement + '|')
    user_regex_string = user_regex_string[:-1] + ')'
    user_regex_string = re.compile(user_regex_string)
    return user_regex_string

def extract_info_from_config(cfg:json):
    return cfg["input-rows"], cfg["input-columns"], cfg["channels"], cfg["movements"], cfg["batch-size"], cfg["train-steps"], cfg["validation-steps"], cfg["test-steps"], cfg["epochs"]

def split_dataset(files:list, cfg:json):
    movements_regex_string = build_regex_for_movement(cfg["movements"])
    # Load train set
    train_user_regex_string = build_regex_for_subjects(cfg["train-subjects"])
    train_files = filter_files_by_regex(files, train_user_regex_string)
    train_files = filter_files_by_regex(train_files, movements_regex_string)
    # Load test set
    test_user_regex_string = build_regex_for_subjects(cfg["test-subjects"])
    test_files = filter_files_by_regex(files, test_user_regex_string)
    test_files = filter_files_by_regex(test_files, movements_regex_string)
    # Use only original files
    test_files = filter_files_by_regex(test_files, r'-0.csv$')

    # Load validation set
    validation_user_regex_string = build_regex_for_subjects(cfg["validation-subjects"])
    validation_files = filter_files_by_regex(files, validation_user_regex_string)
    validation_files = filter_files_by_regex(validation_files, movements_regex_string)
    # Use only original files
    validation_files = filter_files_by_regex(validation_files, r'-0.csv$')

    print("Original train files: " + str(len(filter_files_by_regex(train_files, r'-0.csv$'))))
    print("Total train files: " + str(len(train_files)))
    print("Original validation files: " + str(len(filter_files_by_regex(validation_files, r'-0.csv$'))))
    print("Total validation files: " + str(len(validation_files)))
    print("Original test files: " + str(len(filter_files_by_regex(test_files, r'-0.csv$'))))
    print("Total test files: " + str(len(test_files)))

    return train_files, validation_files, test_files

def balance_data_set(files:list, cfg:json, set:str):
    movement_samples = {}
    for movement in cfg["movements"]:
        movement_regex_string = re.compile(movement)
        files_filtered = filter_files_by_regex(files, movement_regex_string)
        movement_samples[movement] = len(files_filtered)
    min_key = min(movement_samples, key=movement_samples.get)
    final_files = []
    print("Under balancing data-set by movement " + min_key + " with " +  str(movement_samples[min_key]) + " total files.")
    for movement in cfg["movements"]:
        movement_regex_string = re.compile(movement)
        files_filtered = filter_files_by_regex(files, movement_regex_string)
        random.shuffle(files_filtered)
        final_files = final_files + files_filtered[:movement_samples[min_key]]
    print("Final " + set + " data-set has " + str(len(final_files)) + " images.")
    return final_files

def loadCfgJson(file_path:str):
     with open(file_path) as f:
        return json.load(f)

def create_folder(folder_path: str):
    datetime_object = datetime.datetime.now()
    folder_path = folder_path + '/' + str(datetime_object)
    os.mkdir(folder_path)
    return folder_path

def create_outcome_file(outcome_path:str, model, test_loss, test_accuracy, history_callback):
    history = history_callback.history
    with open(outcome_path + '/outcome.txt', 'w') as file:
        file.write('##################################################\n')
        file.write('#                 MODEL SUMMARY                  #\n') 
        file.write('##################################################\n')
        
        model.summary(print_fn=lambda x: file.write(x + '\n'))
        
        file.write('\n\n')
        file.write('##################################################\n')
        file.write('#                 TRAIN OUTCOME                  #\n') 
        file.write('##################################################\n')


        for i in range(len(history["loss"])):
            file.write( 'loss: ' +  str(format(history["loss"][i], ".4f")) + 
            ' | accuracy: ' +  str(format(history["accuracy"][i], ".4f")) + 
            ' | val_loss: ' +  str(format(history["val_loss"][i], ".4f")) +
            ' | val_accuracy: ' +  str(format(history["val_accuracy"][i], ".4f")) + '\n')

        file.write('\n\n')
        file.write('##################################################\n')
        file.write('#                 TEST OUTCOME                   #\n') 
        file.write('##################################################\n')
        file.write( 'loss: ' +  str(format(test_loss, ".4f")) + ' | accuracy: ' +  str(format(test_accuracy, ".4f")))

        file.write('\n\n')
        file.write('##################################################\n')
        file.write('#                     NOTES                      #\n') 
        file.write('##################################################\n')
        file.write('\n\n')
      
def create_config_output_file(outcome_path:str, cfg:json):
    with open(outcome_path + '/config.json', 'w') as outfile:
        json.dump(cfg, outfile)

def save_model_and_weights(outcome_path:str, model):
    model_json = model.to_json()
    with open(outcome_path + '/model.json', "w") as json_file:
        json_file.write(model_json)
    model.save_weights(outcome_path + '/model.h5')

def addCallbacks(callbacks:json, callback_list: list):
    for callback in callbacks:
        if(callback["type"] == "earlyStop"):
            callback_list.append(tf.keras.callbacks.EarlyStopping(monitor=callback["monitor"], patience=callback["patience"]))
    return callback_list

def initialize_folder(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

def create_confusion_matrix(prediction:list, file_path:str, movements:list):
    predicted_labels = prediction.argmax(axis=-1)
    with open(file_path+ '/test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        test_labels= []
        for row in csv_reader:
            array = row[0].replace("\n", " ").replace("[", " ").replace("]", " ")[1:]
            for char in array:
                if char.isdigit():
                    test_labels.append(int(char))
        test_labels = np.array(test_labels)
        final_confusion_matrix = confusion_matrix(test_labels, predicted_labels)
    columns = np.array(movements)
    df_cm = pd.DataFrame(final_confusion_matrix,index=columns ,columns=columns)
    fig = plt.figure(figsize = (len(columns),len(columns)))
    sn.set(font_scale=1.4) # for label size
    sn.heatmap(df_cm, annot=True, cmap='Oranges', annot_kws={"size": 10}, fmt="d") # font size
    fig.tight_layout()
    plt.savefig(file_path + '/confusion-matrix.png')
