import copy
import json
import os
import shutil

import numpy as np
import pandas as pd
from toolz import interleave

import enricher_utils as eutils

position_folder_names = []
orientation_folder_names = []

# Porject main directory path
# main_path = os.getcwd()
main_path = '/TFG'

# Loads configuration file
cfg_filename = main_path + '/framework/pre-processing/config.json'
with open(cfg_filename) as f:
  full_config = json.load(f)
  dt_cfg = full_config["in-dt"]
  im_bu_cfg = full_config["image-builder"]
  cfg = full_config["image-enricher"]

# Path to _output file
input_path = main_path + '/framework/pre-processing/image-builder/_output/'
zippedinput_path = main_path + '/framework/image-builder/_output-zipped/'
general_output_path = main_path + '/framework/pre-processing/image-enricher/_output/'
fft_output_path = main_path + '/framework/pre-processing/image-enricher/_output-FFT/'

##################################################################
# Methods                                                        #
################################################################## 
def del_previous_folder():
  for filename in os.listdir(input_path):
    file_path = os.path.join(input_path, filename)
    shutil.rmtree(file_path)

def build_output_directory():
  #Clean output directory
  try:
      shutil.rmtree(output_path+'position')
  except OSError as e:
      print("Error: %s : %s" % (output_path+'position', e.strerror))
  
  #Create postion directories:
  os.mkdir(output_path+'position/')
  for movement in dt_cfg["movements"]["list"]:
    position_folder_names.append(output_path+'position/'+movement+'/')
    os.mkdir(position_folder_names[-1])

  try:
      shutil.rmtree(output_path+'orientation/')
  except OSError as e:
      print("Error: %s : %s" % (output_path+'orientation/', e.strerror))
  
  #Create orientation directories:
  os.mkdir(output_path+'orientation/')
  for movement in dt_cfg["movements"]["list"]:
    orientation_folder_names.append(output_path+'orientation/'+movement+'/')
    os.mkdir(orientation_folder_names[-1])

def fold_images():
    # for position_folder_name in dt_cfg["movements"]["list"]:
    #   print("\nBuilding folded images for position movement: " + position_folder_name)
    #   input_folder = input_path+'position/'+position_folder_name+'/'
    #   output_folder = general_output_path + 'position/' + position_folder_name + '/'
    #   fft_output_folder = fft_output_path + 'position/' + position_folder_name + '/'
    #   _, _, files = next(os.walk(input_folder))
    #   image_size = im_bu_cfg["images"]["window-size"]
    #   sensors_number = len(dt_cfg["positionSensors"]["list"])
    #   column_names = []
    #   for sensor in dt_cfg["positionSensors"]["list"]:
    #       column_names.append(sensor+'-0')
    #       column_names.append(sensor+'-1')
    #       column_names.append(sensor+'-2')
    #   for file in files:
    #       fold_position_image(input_folder+file, output_folder+file, image_size, sensors_number, column_names, fft_output_folder+file, im_bu_cfg, cfg)

    for orientation_folder_name in dt_cfg["movements"]["list"]:
      print("\nBuilding folded images for orientation movement: " + orientation_folder_name)
      input_folder = input_path + 'orientation/' +orientation_folder_name + '/'
      output_folder = output_path + 'orientation/' + orientation_folder_name + '/'
      fft_output_folder = fft_output_path + 'orientation/' + orientation_folder_name + '/'
      _, _, files = next(os.walk(input_folder))
      image_size = im_bu_cfg["images"]["window-size"]
      sensors_number = len(dt_cfg["orientationSensors"]["list"])
      column_names = []
      for sensor in dt_cfg["orientationSensors"]["list"]:
          column_names.append(sensor+'-0')
          column_names.append(sensor+'-1')
          column_names.append(sensor+'-2')
          column_names.append(sensor+'-3')
      total_number = len(files)
      percentage,_ = divmod(total_number*0.25, 1)
      for file in files:
          eutils.fold_orientation_image(input_folder+file, output_folder+file, image_size, sensors_number, column_names, fft_output_folder+file, im_bu_cfg, cfg)
          total_number = total_number - 1
          if(total_number % percentage == 0):
            print( "   - " + str(total_number) + " files remaining")

def table-images():
    for orientation_folder_name in dt_cfg["movements"]["list"]:
      print("\nBuilding folded images for orientation movement: " + orientation_folder_name)
      input_folder = input_path + 'orientation/' +orientation_folder_name + '/'
      output_folder = output_path + 'orientation/' + orientation_folder_name + '/'
      fft_output_folder = fft_output_path + 'orientation/' + orientation_folder_name + '/'
      _, _, files = next(os.walk(input_folder))
      image_size = im_bu_cfg["images"]["window-size"]
      sensors_number = len(dt_cfg["orientationSensors"]["list"])
      column_names = []
      for sensor in dt_cfg["orientationSensors"]["list"]:
          column_names.append(sensor+'-0')
          column_names.append(sensor+'-1')
          column_names.append(sensor+'-2')
          column_names.append(sensor+'-3')
      total_number = len(files)
      for file in files:
          eutils.table_orientation_image(input_folder+file, output_folder+file, image_size, sensors_number, column_names, fft_output_folder+file, cfg)
          print( "   - " + str(total_number) + " files remaining")
          total_number = total_number - 1

#########################
# Main                  #
#########################
if cfg["FFT"]["enabled"]:
  # Prepare output directory for images with FFT
  output_path = fft_output_path
  build_output_directory()

if cfg["deepen-images"]["enabled"]:
  # Prepare output directory
  output_path = general_output_path
  build_output_directory()
  fold_images()

# Trial/draft not working
if cfg["table-images"]["enabled"]:
  # Prepare output directory
  output_path = general_output_path
  table-images()

print("\nIMAGE ENRICHMENT FINISHED")

if cfg["deletePrevious"]:
  del_previous_folder
