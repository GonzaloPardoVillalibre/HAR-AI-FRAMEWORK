from toolz import interleave
import os
import pandas as pd
import json
import shutil
import numpy as np 

position_folder_names = []
orientation_folder_names = []

# Porject main directory path
main_path = os.getcwd()

# Loads configuration file
cfg_filename = main_path + '/vicon/pre-processing/config.json'
with open(cfg_filename) as f:
  full_config = json.load(f)
  dt_cfg = full_config["1"]["in-dt"]
  im_bu_cfg = full_config["1"]["im-bu"]
  cfg = full_config["1"]["im-en"]

# Path to _output file
input_path = main_path + '/vicon/pre-processing/image-builder/_output/'
zippedinput_path = main_path + '/vicon/image-builder/_output-zipped/'
output_path = main_path + '/vicon/pre-processing/image-enricher/_output/'


def build_output_directory():
  #Clean output directory
  shutil.rmtree(output_path+'position/')
  shutil.rmtree(output_path+'orientation/')

  #Create postion directories:
  os.mkdir(output_path+'position/')
  for movement in dt_cfg["movements"]["list"]:
    position_folder_names.append(output_path+'position/'+movement+'/')
    os.mkdir(position_folder_names[-1])

  #Create orientation directories:
  os.mkdir(output_path+'orientation/')
  for movement in dt_cfg["movements"]["list"]:
    orientation_folder_names.append(output_path+'orientation/'+movement+'/')
    os.mkdir(orientation_folder_names[-1])

def fold_position_image(input_file: str, output_file: str, image_size, sensors_number, column_names: list):
    print("\nFolding image: " + input_file)
    df = pd.read_fwf(input_file, header=None)
    df = df[0].str.split(',', expand=True)
    df = df.iloc[1:]
    df = df.drop(df.columns[[0, 1]], axis=1)
    image_size = im_bu_cfg["images"]["batch-size"]
    final_df = pd.DataFrame(df.values.reshape(image_size, sensors_number*3), columns=column_names)
    final_df.to_csv(output_file)


def fold_images():
    for position_folder_name in dt_cfg["movements"]["list"]:
        input_folder = input_path+'position/'+position_folder_name+'/'
        output_folder = output_path+'position/'+position_folder_name+'/'
        _, _, files = next(os.walk(input_folder))
        image_size = im_bu_cfg["images"]["batch-size"]
        sensors_number = len(dt_cfg["positionSensors"]["list"])
        column_names = []
        for sensor in dt_cfg["positionSensors"]["list"]:
            column_names.append(sensor+'-0')
            column_names.append(sensor+'-1')
            column_names.append(sensor+'-2')
        for file in files:
            fold_position_image(input_folder+file, output_folder+file, image_size, sensors_number, column_names)
    # for orientation_folder_names in dt_cfg["movements"]["list"]:
    #     fold_orientation_images()

#########################
# Main                  #
#########################
if cfg["deepen_images"]["enabled"]:
  # Prepare output directory
  build_output_directory()

  
  fold_images()


print("\nIMAGE ENRICHMENT FINISHED")
