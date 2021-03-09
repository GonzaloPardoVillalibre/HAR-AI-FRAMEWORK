import os
import shutil
import json
import random
import re
# Porject main directory path
# main_path = os.getcwd()
main_path = '/TFG'

position_folder_names = []
orientation_folder_names = []

# Loads configuration file
cfg_filename = main_path + '/framework/pre-processing/config.json'
not_mixed_input = main_path + '/framework/pre-processing/image-enricher/_output/'
fft_input = main_path + '/framework/pre-processing/image-enricher/_output-FFT/'
final_output_path = main_path + '/framework/final-dataset/'

with open(cfg_filename) as f:
  full_config = json.load(f)
  dt_cfg = full_config["in-dt"]
  im_bu_cfg = full_config["im-bu"]
  im_en_cfg = full_config["im-en"]
  cfg = full_config["final-dataset"]

# The input depends if we want to use the FFT results or not
if cfg["FFT-input"]:
  input_path = fft_input
else:
  input_path = not_mixed_input

##################################################################
# Methods                                                        #
################################################################## 
def build_output_directory():
  #Clean output directory
  try:
    shutil.rmtree(final_output_path+'position')
    os.mkdir(final_output_path+'position')
    shutil.rmtree(final_output_path+'orientation')
    os.mkdir(final_output_path+'orientation')
  except:
    print("No folder had to be removed")

    
def move_files_to_folder(input:str, output:str, files:[]):
  for file in files:
    shutil.move(input+file, output+file)

def create_orientation_final_dataset():
  for movement in cfg["movements"]["list"]:
    orientation_input_path = input_path + 'orientation/'+movement+'/'
    orientation_final_output_path =  final_output_path +'orientation/'
    _, _, files = next(os.walk(orientation_input_path))
    original_list =[val for val in files if re.search(r'-0.csv$', val)]
    print("Total original orientation images for movement " + movement + " : " + str(len(original_list)))
    print("Total orientation images for movement " + movement + " : " + str(len(files)))
    move_files_to_folder(orientation_input_path, orientation_final_output_path, files)

def create_position_final_dataset():
  for movement in cfg["movements"]["list"]:
    position_input_path = input_path + 'position/'+movement+'/'
    position_final_output_path = final_output_path +'position/'
    _, _, files = next(os.walk(position_input_path))
    original_list =[val for val in files if re.search(r'-0.csv$', val)]
    print("Total original position images for movement " + movement + " : " + str(len(original_list)))
    print("Total position images for movement " + movement + " : " + str(len(files)))
    # move_files_to_folder(position_input_path, position_final_output_path, files)

#########################
# Main                  #
#########################
build_output_directory()
# create_position_final_dataset()
create_orientation_final_dataset()
