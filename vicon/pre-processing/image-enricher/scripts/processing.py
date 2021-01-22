from toolz import interleave
import os
import pandas as pd
import json
import shutil
import numpy as np
import copy

position_folder_names = []
orientation_folder_names = []

# Porject main directory path
main_path = os.getcwd()

# Loads configuration file
cfg_filename = main_path + '/vicon/pre-processing/config.json'
with open(cfg_filename) as f:
  full_config = json.load(f)
  dt_cfg = full_config["in-dt"]
  im_bu_cfg = full_config["im-bu"]
  cfg = full_config["im-en"]

# Path to _output file
input_path = main_path + '/vicon/pre-processing/image-builder/_output/'
zippedinput_path = main_path + '/vicon/image-builder/_output-zipped/'
general_output_path = main_path + '/vicon/pre-processing/image-enricher/_output/'
fft_output_path = main_path + '/vicon/pre-processing/image-enricher/_output-FFT/'

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
    print("No folder had to be removed")

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

def build_and_save_image_with_FFT(df: pd.DataFrame, fft_output_file: str):
    names = df.columns.values
    data = df.values
    data = data.astype(np.float32)
    data = np.fft.fft2(data)
    fft_df_real = pd.DataFrame(data.real.astype(np.float32), columns=names)
    fft_df_imag = pd.DataFrame(data.imag.astype(np.float32), columns=names)
    if cfg["FFT"]["combined"]:
      fft_df = pd.concat([df, fft_df_real, fft_df_imag], axis=1)
    fft_df.to_csv(fft_output_file)

def unitary_rotation_quaternion(x:float, y:float, z:float, a:float):
  rotation_factor = np.sin( a / 2.0 )
  x = x * rotation_factor
  y = y * rotation_factor
  z = z * rotation_factor
  w = np.cos( a / 2 )
  return [w,x,y,z]

def quaternion_multiply(quaternion1, quaternion0):
    w0, x0, y0, z0 = quaternion0
    w1, x1, y1, z1 = quaternion1
    return np.array([-x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0,
                     x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0,
                     -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0,
                     x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0], dtype=np.float32)

def create_rotated_images(grades, original_df):
  vector_de_rotacion =  unitary_rotation_quaternion(0,0,1, grades*np.pi/180)
  original_df_array = original_df.values
  final_df_array = copy.deepcopy(original_df_array)
  i = 0
  for element in original_df_array:
    final_df_array[i] = quaternion_multiply(element, vector_de_rotacion)
    i = i +1
  return final_df_array

def fold_position_image(input_file: str, output_file: str, image_size, sensors_number, column_names: list, fft_output_file: str):
    df = pd.read_csv(input_file, header=None)
    df = df.iloc[1:]
    df = df.drop(df.columns[[0, 1]], axis=1)
    df = df.astype(np.float32)
    image_size = im_bu_cfg["images"]["batch-size"]
    final_df = pd.DataFrame(df.values.reshape(image_size, sensors_number*3), columns=column_names)
    if cfg["FFT"]["enabled"]:
      build_and_save_image_with_FFT(final_df, fft_output_file)
    if cfg["FFT"]["saveWithoutFFT"]:
      final_df.to_csv(output_file)

def fold_orientation_image(input_file: str, output_file: str, image_size, sensors_number, column_names: list, fft_output_file: str):
    df = pd.read_csv(input_file, header=None)
    df = df.iloc[1:]
    df = df.drop(df.columns[[0, 1]], axis=1)
    df = df.astype(np.float32)
    image_size = im_bu_cfg["images"]["batch-size"]
    for rotation_grades in cfg["dataAugmentationRotation"]["gradeList"]:
      rotated_df = create_rotated_images(rotation_grades, df)
      final_df = pd.DataFrame(rotated_df.reshape(image_size, sensors_number*4), columns=column_names)
      if cfg["FFT"]["enabled"]:
        build_and_save_image_with_FFT(final_df, fft_output_file + '-' + str(rotation_grades))
      if cfg["FFT"]["saveWithoutFFT"]:
        final_df.to_csv(output_file + '-' + str(rotation_grades))

def fold_images():
    # for position_folder_name in dt_cfg["movements"]["list"]:
    #   print("\nBuilding folded images for position movement: " + position_folder_name)
    #   input_folder = input_path+'position/'+position_folder_name+'/'
    #   output_folder = general_output_path + 'position/' + position_folder_name + '/'
    #   fft_output_folder = fft_output_path + 'position/' + position_folder_name + '/'
    #   _, _, files = next(os.walk(input_folder))
    #   image_size = im_bu_cfg["images"]["batch-size"]
    #   sensors_number = len(dt_cfg["positionSensors"]["list"])
    #   column_names = []
    #   for sensor in dt_cfg["positionSensors"]["list"]:
    #       column_names.append(sensor+'-0')
    #       column_names.append(sensor+'-1')
    #       column_names.append(sensor+'-2')
    #   for file in files:
    #       fold_position_image(input_folder+file, output_folder+file, image_size, sensors_number, column_names, fft_output_folder+file)

    for orientation_folder_name in dt_cfg["movements"]["list"]:
      print("\nBuilding folded images for orientation movement: " + orientation_folder_name)
      input_folder = input_path + 'orientation/' +orientation_folder_name + '/'
      output_folder = output_path + 'orientation/' + orientation_folder_name + '/'
      fft_output_folder = fft_output_path + 'orientation/' + orientation_folder_name + '/'
      _, _, files = next(os.walk(input_folder))
      image_size = im_bu_cfg["images"]["batch-size"]
      sensors_number = len(dt_cfg["orientationSensors"]["list"])
      column_names = []
      for sensor in dt_cfg["orientationSensors"]["list"]:
          column_names.append(sensor+'-0')
          column_names.append(sensor+'-1')
          column_names.append(sensor+'-2')
          column_names.append(sensor+'-4')
      total_number = len(files)
      for file in files:
          fold_orientation_image(input_folder+file, output_folder+file, image_size, sensors_number, column_names, fft_output_folder+file)
          print( "   - " + str(total_number) + " files remaining")
          total_number = total_number - 1

#########################
# Main                  #
#########################
if cfg["FFT"]["enabled"]:
  # Prepare output directory for images with FFT
  output_path = fft_output_path
  build_output_directory()

if cfg["deepen_images"]["enabled"]:
  # Prepare output directory
  output_path = general_output_path
  build_output_directory()
  fold_images()

print("\nIMAGE ENRICHMENT FINISHED")

if cfg["deletePrevious"]:
  del_previous_folder