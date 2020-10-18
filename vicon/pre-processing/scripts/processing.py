from toolz import interleave
import os
import pandas as pd
import json


# Porject main directory path
main_path = os.getcwd()

# Loads configuration file
cfg_filename = main_path + '/vicon/pre-processing/scripts/config.json'
with open(cfg_filename) as f:
  cfg = json.load(f)

# Path to _output file
output_path = main_path + '/vicon/pre-processing/_output/'

##################################################################
# Methods                                                        #
##################################################################

# Extracts orientation information for each line in csv
def extract_quat_columns(file, jointName):
    df = pd.read_fwf(file, header=None)
    df = df[0].str.split(',', expand=True)
    df.columns = df.iloc[5]
    df = df.drop(axis=0, index=[0, 1, 2, 3, 4, 5])
    df = df.filter(regex=jointName)
    df.insert(loc=0, column='quat', value=jointName)
    df.columns = ['quat', '0', '1', '2', '3']
    return df

# Extracts position information for each line in csv
def extract_position_columns(file, jointName):
    df = pd.read_fwf(file, header=None)
    df = df[0].str.split(',', expand=True)
    df.columns = df.iloc[5]
    df = df.drop(axis=0, index=[0, 1, 2, 3, 4, 5])
    df = df.filter(regex=jointName)
    df.insert(loc=0, column='3D vecotr', value=jointName)
    df.columns = ['3D vecotr', '0', '1', '2']
    return df

# Builds composed datatable for all sensors and one movement
# Saves the new csv with the following data:
#   - Rows: original * number of sensors in the list.
#   - Columns: 4 in orientation sensors, 3 in position.
def build_dt(sample: str, subject: str, movement: str):
  subject_and_activity_file =  main_path + '/vicon/dataset/' + subject + '-Trial-' + movement + '-' + sample + '.csv'
  orientation_df_list = list()
  position_df_list = list()

  # Check file exists
  try:
    f = open(subject_and_activity_file)
    f.close()
  except FileNotFoundError:
    print("      WARNING: File not accessible!")
    return
    
  if cfg["orientationSensors"]["enabled"]: 
    jointNamesListVicon = cfg["orientationSensors"]["list"]
    for sensor in jointNamesListVicon:
        df = extract_quat_columns(subject_and_activity_file, sensor)
        orientation_df_list.append(df.values)
    final_df = pd.DataFrame(interleave(orientation_df_list))
    subject_and_activity_file_output = output_path + subject + '-' + movement + '-Orientationjoints-' + sample + '.csv'
    final_df.to_csv(subject_and_activity_file_output)

  if cfg["positionSensors"]["enabled"]: 
    jointNamesListVicon = cfg["positionSensors"]["list"]
    for sensor in jointNamesListVicon:
        df = extract_position_columns(subject_and_activity_file, sensor)
        position_df_list.append(df.values)
    final_df = pd.DataFrame(interleave(position_df_list))
    subject_and_activity_file_output = output_path + subject + '-' + movement + '-Positionjoints-' + sample + '.csv'
    final_df.to_csv(subject_and_activity_file_output)

# Analizes configured movements and samples
def  create_dt_by_movement(subject: str):
  print("Building images for subject: " + subject)
  for movement in cfg["movements"]["list"]:
    for sample in cfg["movements"]["samples"]:
      print("   Movement " + movement + " & record sample " + sample)
      build_dt(sample, subject, movement)

#########################
# Main                  #
#########################
for subject in cfg["subjects"]["list"]:
  create_dt_by_movement(subject)
print("\nPRE-PROCESSING FINISHED")