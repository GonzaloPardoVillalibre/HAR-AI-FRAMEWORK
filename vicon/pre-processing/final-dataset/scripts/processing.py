import os
import shutil
import json
import random
# Porject main directory path
main_path = os.getcwd()

position_folder_names = []
orientation_folder_names = []

# Loads configuration file
cfg_filename = main_path + '/vicon/pre-processing/config.json'
not_mixed_input = main_path + '/vicon/pre-processing/image-enricher/_output/'
fft_input = main_path + '/vicon/pre-processing/image-enricher/_output-FFT/'
test_output_path = main_path + '/vicon/pre-processing/final-dataset/test-set/'
train_output_path = main_path + '/vicon/pre-processing/final-dataset/train-set/'
validation_output_path = main_path + '/vicon/pre-processing/final-dataset/validation-set/'

with open(cfg_filename) as f:
  full_config = json.load(f)
  dt_cfg = full_config["1"]["in-dt"]
  im_bu_cfg = full_config["1"]["im-bu"]
  im_en_cfg = full_config["1"]["im-en"]
  cfg = full_config["1"]["final-dataset"]

# The input depends if we want to use the FFT results or not
if cfg["FFT-input"]:
  input_path = fft_input
else:
  input_path = not_mixed_input

##################################################################
# Methods                                                        #
################################################################## 
def del_previous_folder():
  for filename in os.listdir(input_path):
    try: 
      file_path = os.path.join(input_path, filename)
      shutil.rmtree(file_path)
    except:
      print("Not a directory")

def build_output_directory_by_percentage():
  #Clean output directory
  try:
    shutil.rmtree(test_output_path+'position/')
    shutil.rmtree(test_output_path+'orientation/')
    shutil.rmtree(train_output_path+'position/')
    shutil.rmtree(train_output_path+'orientation/')
  except:
    print("No folder had to be removed")

def build_output_directory_by_subjects():
  #Clean output directory
  try:
    shutil.rmtree(test_output_path)
    shutil.rmtree(train_output_path)
    shutil.rmtree(validation_output_path)
  except:
    print("No folder had to be removed")

    os.mkdir(test_output_path)
    os.mkdir(train_output_path)
    os.mkdir(validation_output_path)

def move_files_to_folder(input:str, output:str, files:[]):
  for file in files:
    shutil.copy(input+file, output+file)

def create_orientation_final_dataset_by_percentage():
  for movement in cfg["movements"]["list"]:
      orientation_input_path = input_path + 'orientation/'+movement+'/'
      orientation_train_output_path = train_output_path +'orientation/'+movement+'/'
      orientation_test_output_path = test_output_path +'orientation/'+movement+'/'
      _, _, files = next(os.walk(orientation_input_path))
      random.shuffle(files)
      length = len(files)
      print("Total orientation images for movement " + movement + " : " + str(length))
      index = int((length*cfg["trainPercentage"])//1)
      train_list = files[:index]
      move_files_to_folder(orientation_input_path, orientation_train_output_path, train_list)
      test_list =  files[index:]
      move_files_to_folder(orientation_input_path, orientation_test_output_path, test_list)
      print("Final orientation dataset for movement " + movement + " created successfully")

def create_position_final_dataset_by_perecentage():
  for movement in cfg["movements"]["list"]:
      position_input_path = input_path + 'position/'+movement+'/'
      position_train_output_path = train_output_path +'position/'+movement+'/'
      position_test_output_path = test_output_path +'position/'+movement+'/'
      _, _, files = next(os.walk(position_input_path))
      random.shuffle(files)
      length = len(files)
      print("Total position images for movement " + movement + " : " + str(length))
      index = int((length*cfg["trainPercentage"])//1)
      train_list = files[:index]
      move_files_to_folder(position_input_path, position_train_output_path, train_list)
      test_list =  files[index:]
      move_files_to_folder(position_input_path, position_test_output_path, test_list)
      print("Final position dataset for movement " + movement + " created successfully")

def create_orientation_final_dataset_by_subjects():
  for movement in cfg["movements"]["list"]:
      test_list = []
      total_train_list = []
      orientation_input_path = input_path + 'orientation/'+movement+'/'
      _, _, files = next(os.walk(orientation_input_path))
      for file in files:
        for subject in cfg["bySubjects"]["test-subjects"]:
          if subject not in cfg["bySubjects"]["obviate"][movement]:
            if subject in file:
                test_list.append(file)
      for file in files:
        for subject in cfg["bySubjects"]["train-subjects"]:
          if subject not in cfg["bySubjects"]["obviate"][movement]:
            if subject in file:
                total_train_list.append(file)
      random.shuffle(total_train_list)
      length = len(total_train_list)
      print("Total training orientation images for movement " + movement + " : " + str(length))
      index = int((length*cfg["bySubjects"]["validationPercentage"])//1)
      validation_list = total_train_list[:index]
      train_list =  total_train_list[index:]
      move_files_to_folder(orientation_input_path, validation_output_path, validation_list)
      move_files_to_folder(orientation_input_path, train_output_path, train_list)
      move_files_to_folder(orientation_input_path, test_output_path, test_list)
      print("Final orientation dataset for movement " + movement + " created successfully")
 
#########################
# Main                  #
#########################
if cfg["byPercentage"]["enabled"]:
  build_output_directory_by_percentage()
  create_orientation_final_dataset_by_percentage()
  create_position_final_dataset_by_perecentage()

if cfg["bySubjects"]["enabled"]:
  build_output_directory_by_subjects()
  create_orientation_final_dataset_by_subjects()

if cfg["deletePrevious"]:
  del_previous_folder()
