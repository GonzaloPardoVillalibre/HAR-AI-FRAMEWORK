from toolz import interleave
import os
import pandas as pd
import json, sys

# Current file path
current_path = os.path.dirname(os.path.abspath(__file__))
interleaved_df_path = current_path + '/..'
cfg_filename = interleaved_df_path + '/unityConfig.json'

# Path to _output file
output_path = interleaved_df_path + '/_output/'
zippedoutput_path = interleaved_df_path + '/_output-zipped/'

# Load file utils file
sys.path.append(current_path + '/../../utils')
import fileUtils

# Loads configuration file
with open(cfg_filename) as f:
  cfg = json.load(f)

# Extracts orientation information for each line in csv
def extract_quat_columns(file, jointName):
    df = pd.read_csv(file, header=None)
    first_row = df.iloc[0].values
    df = df.iloc[1:]
    df.columns = first_row
    df = df.filter(regex=jointName)
    df = df[:].astype(float)
    df.insert(loc=0, column='quat', value=jointName)
    df.columns = ['quat', '0', '1', '2', '3']
    return df

# Extracts position information for each line in csv
def extract_position_columns(file, jointName):
    df = pd.read_csv(file, header=None)
    first_row = df.iloc[0].values
    df = df.iloc[1:]
    df.columns = first_row
    df = df.filter(regex=jointName)
    df = df[:].astype('float32')
    df.insert(loc=0, column='3D vector', value=jointName)
    df.columns = ['3D vecotr', '0', '1', '2']
    return df

# Builds composed datatable for all sensors and one activities
# Saves the new csv with the following data:
#   - Rows: original * number of sensors in the list.
#   - Columns: 4 in orientation sensors, 3 in position.
def build_dt(sample: str, subject: str, movement: str):
  subject_and_activity_file =  interleaved_df_path + '/../dataset/' + subject + '-' + movement + '-' + sample + '.csv'
  orientation_df_list = list()
  position_df_list = list()

  # Check file exists
  try:
    f = open(subject_and_activity_file)
    f.close()
  except FileNotFoundError:
    print("      WARNING: File not accessible!")
    return
    
  if cfg["4D-Sensors"]["enabled"]: 
    jointNamesListVicon = cfg["4D-Sensors"]["list"]
    for sensor in jointNamesListVicon:
        df = extract_quat_columns(subject_and_activity_file, sensor)
        orientation_df_list.append(df.values)
    final_df = pd.DataFrame(interleave(orientation_df_list))
    subject_and_activity_file_output = output_path + subject + '-' + movement + '-Orientationjoints-' + sample + '.csv'
    final_df.to_csv(subject_and_activity_file_output, index=False)

  if cfg["3D-Sensors"]["enabled"]: 
    jointNamesListVicon = cfg["3D-Sensors"]["list"]
    for sensor in jointNamesListVicon:
        df = extract_position_columns(subject_and_activity_file, sensor)
        position_df_list.append(df.values)
    final_df = pd.DataFrame(interleave(position_df_list))
    subject_and_activity_file_output = output_path + subject + '-' + movement + '-Positionjoints-' + sample + '.csv'
    final_df.to_csv(subject_and_activity_file_output, index=False)

# Analyzes configured activities and samples
def  create_dt_by_movement(subject: str):
  print("Building interleaved dataframes for subject: " + subject)
  for movement in cfg["activities"]["list"]:
    for sample in cfg["activities"]["samples"]:
      print("   Movement " + movement + " & record sample " + sample)
      build_dt(sample, subject, movement)

# Creates the so called "interleved dataframe" for Unity 3D representation.
#########################
# Main                  #
#########################
fileUtils.build_output_directory(output_path)
for subject in cfg["subjects"]["list"]:
  create_dt_by_movement(subject)
print("\nINTERLEAVED DATAFRAMES BUILDING FINISHED")
