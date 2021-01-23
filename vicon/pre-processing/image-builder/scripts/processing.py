from toolz import interleave
import os
import pandas as pd
import json
import shutil 

global  orientation_image_number

# Porject main directory path
# main_path = os.getcwd()
main_path = '/TFG'

# Loads configuration file
cfg_filename = main_path + '/vicon/pre-processing/config.json'
with open(cfg_filename) as f:
  full_config = json.load(f)
  dt_cfg = full_config["in-dt"]
  cfg = full_config["im-bu"]

# Path to _output file
input_path = main_path + '/vicon/pre-processing/interleaved-dataframe/_output/'
zippedinput_path = main_path + '/vicon/pre-processing/interleaved-dataframe/_output-zipped/'
output_path = main_path + '/vicon/pre-processing/image-builder/_output/'

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
    shutil.rmtree(output_path+'position/')
    shutil.rmtree(output_path+'orientation/')
  except: 
    print("No folders to be removed")
    
  #Create postion directories:
  os.mkdir(output_path+'position/')
  for movement in dt_cfg["movements"]["list"]:
    os.mkdir(output_path+'position/'+movement+'/')

  #Create orientation directories:
  os.mkdir(output_path+'orientation/')
  for movement in dt_cfg["movements"]["list"]:
    os.mkdir(output_path+'orientation/'+movement+'/')

def path_to_save(file: str, sensorType:str):
  for movement in dt_cfg["movements"]["list"]:
    if movement in file:
      return output_path + sensorType + movement + '/'

def load_files():
  _, _, files = next(os.walk(input_path))
  try:
    files.remove('config.json')
  except :
    print("config.json not in list")
  return files

def calculate_sample_size():
  global orientation_sample_size
  global position_sample_size
  global orientation_sample_size_overlap
  global position_sample_size_overlap
  sensors_size =  len(dt_cfg["orientationSensors"]["list"])
  batch_size = cfg["images"]["batch-size"]
  overlap = cfg["images"]["overlap"]
  orientation_sample_size = sensors_size * batch_size
  orientation_sample_size_overlap = overlap * sensors_size
  if not isinstance(orientation_sample_size_overlap, int):
    print("overlap * orientation_sensors_size must be int")
    exit
  sensors_size =  len(dt_cfg["positionSensors"]["list"])
  position_sample_size = sensors_size * batch_size
  position_sample_size_overlap = overlap * sensors_size
  if not isinstance(position_sample_size_overlap, int):
    print("overlap * position_sensors_size must be int")
    exit

def build_position_images(file: str):
  print("Building images for posititon file: " + file)
  df = pd.read_csv(input_path + file, header=None)
  # Calculate image sizing
  df_len = len(df)
  jump_diff = position_sample_size - position_sample_size_overlap
  images_number = df_len//jump_diff
  # Build individual images
  for i in range(images_number):
    final_df = df.iloc[(i*jump_diff)+1:(i*jump_diff)+ 1 + position_sample_size]
    del final_df[0]
    final_df.columns = ['3D vecotr', '0', '1', '2']
    final_df[['0', '1', '2']] = final_df[['0', '1', '2']].astype(float)
    if (len(final_df) == position_sample_size):
      path = path_to_save(file, 'position/')
      if path != None:
        image_name = path + file[:-4] +'-' + str(i+1) + '.csv'
        final_df.to_csv(image_name)

def build_orientation_images(file:str):
  print("Building images for orientation file: " + file)
  df = pd.read_csv(input_path + file, header=None)
  # Calculate image sizing
  df_len = len(df)
  jump_diff = orientation_sample_size - orientation_sample_size_overlap
  images_number = df_len//jump_diff
  # Build individual images
  for i in range(images_number):
    final_df = df.iloc[(i*jump_diff)+1:(i*jump_diff)+1 + orientation_sample_size]
    del final_df[0]
    final_df.columns = ['quat', '0', '1', '2', '3']
    final_df[['0', '1', '2', '3']] = final_df[['0', '1', '2', '3']].astype(dtype=float)
    if (len(final_df) == orientation_sample_size):
      path = path_to_save(file, 'orientation/')
      if path != None:
        image_name= path + str(file[:-4]) +'-' + str(i+1) + '.csv'
        final_df.to_csv(image_name )

def build_images(files : str):
  if 'Position' in files and cfg["positionSensors"]["enabled"]:
    build_position_images(file)
  if 'Orientation' in files and cfg["orientationSensors"]["enabled"]:
    build_orientation_images(file)

#########################
# Main                  #
#########################
if cfg["enabled"]:
  if cfg["interleavedOutput"]["useOlder"]["enabled"]:
    # TO DO unzip old file in /tmp to use
    # input_path = this tmp folder
    # cfg = stored_CFG
    print('Using zipped output')
  else:
    print('Using non zipped output')
    files = load_files()
  
  # Prepare output directory
  build_output_directory()

  # Calculate sample size
  calculate_sample_size()

  # Build images
  for file in files:
      build_images(file)

  print("\nIMAGE BUILDING FINISHED")
else:
  print("\nIMAGE BUILDING DISABLED")

if cfg["deletePrevious"]:
  del_previous_folder