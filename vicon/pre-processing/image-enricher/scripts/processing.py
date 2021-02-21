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
# main_path = os.getcwd()
main_path = '/TFG'

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

def split_in_layers(df: pd.DataFrame):
  print("Test how 4D input matrixes will enter the cnn")
  sensors_number = len(dt_cfg["orientationSensors"]["list"])
  test = df.values.reshape(256,sensors_number*3,4)
  filtered_df_1 = df.filter(regex='-0$', axis=1).values
  tu = filtered_df_1.shape[1]
  filtered_df_2 = df.filter(regex='-1$', axis=1).values
  filtered_df_3 = df.filter(regex='-2$', axis=1).values
  filtered_df_4 = df.filter(regex='-3$', axis=1).values
  test2 =  np.stack((filtered_df_1, filtered_df_2, filtered_df_3, filtered_df_4))
  test3 = test2.reshape(256,sensors_number*3,4)
  return df

def build_and_save_image_with_FFT(df: pd.DataFrame, fft_output_file: str):
  names = df.columns.values
  data = df.values
  data = data.astype(np.float32)
  data = np.fft.fft2(data)
  fft_df_real = pd.DataFrame(data.real.astype(np.float32), columns=names)
  fft_df_imag = pd.DataFrame(data.imag.astype(np.float32), columns=names)
  if cfg["FFT"]["combined"]:
    fft_df = pd.concat([df, fft_df_real, fft_df_imag], axis=1)
  # test = split_in_layers(fft_df)
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
    final_df_array[i] = quaternion_multiply(vector_de_rotacion, element)
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
        build_and_save_image_with_FFT(final_df, fft_output_file[:-4] + '-' + str(rotation_grades) + '.csv')
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
          column_names.append(sensor+'-3')
      total_number = len(files)
      for file in files:
          fold_orientation_image(input_folder+file, output_folder+file, image_size, sensors_number, column_names, fft_output_folder+file)
          print( "   - " + str(total_number) + " files remaining")
          total_number = total_number - 1

def table_images():
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
          column_names.append(sensor+'-3')
      total_number = len(files)
      for file in files:
          table_orientation_image(input_folder+file, output_folder+file, image_size, sensors_number, column_names, fft_output_folder+file)
          print( "   - " + str(total_number) + " files remaining")
          total_number = total_number - 1

def table_orientation_image(input_file: str, output_file: str, image_size, sensors_number, column_names: list, fft_output_file: str):
    df = pd.read_csv(input_file, header=None)
    df = df.iloc[1:]
    df = df.drop(df.columns[[0, 1]], axis=1)
    df = df.astype(np.float32)
    for rotation_grades in cfg["dataAugmentationRotation"]["gradeList"]:
      rotated_array = create_rotated_images(rotation_grades, df)
      rotated_df = pd.DataFrame(data=rotated_array)
      total_cells = cfg["table_images"]["size"]
      df_cells = {}
      i = 0
      for cell in range(total_cells*total_cells):
        cell = rotated_df.iloc[(i*7): 7*(i+1)]
        cell = cell.reset_index(drop=True)
        df_cells[i+1] = cell
        i = i +1
      df_rows = {}
      for row in range(total_cells):
        row_selector = cfg["table_images"]["table"][row]
        df_row = df_cells[row_selector[0]]
        for cell in range(total_cells-1):
          prueba2 = df_cells[row_selector[cell+1]].values
          df_row = pd.concat([df_row, df_cells[row_selector[cell+1]]], ignore_index=True, axis=1)
          prueba3 = df_row.values
        df_rows[row] = df_row
      final_df = df_rows[0]
      for row in range(total_cells-1):
        final_df = pd.concat([final_df, df_rows[row+1]], ignore_index=True, axis=0)
      if cfg["FFT"]["enabled"]:
        build_and_save_image_with_FFT(final_df, fft_output_file[:-4] + '-' + str(rotation_grades) + '.csv')
      if cfg["FFT"]["saveWithoutFFT"]:
        final_df.to_csv(output_file + '-' + str(rotation_grades))

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

if cfg["table_images"]["enabled"]:
  # Prepare output directory
  output_path = general_output_path
  table_images()

print("\nIMAGE ENRICHMENT FINISHED")

if cfg["deletePrevious"]:
  del_previous_folder