from toolz import interleave
import os
import pandas as pd
import json, sys
import dataFilteringUtils
import progressbar

# Current file path
current_path = os.path.dirname(os.path.abspath(__file__))
cfg_filename = current_path + '/../pipelineConfig.json'

# Path to _output file
output_path = current_path + '/_output/'

# Input path
input_path = current_path + '/../../dataset/'

# Load file utils file
sys.path.append(current_path + '/../../utils')
import fileUtils

# Loads configuration file
with open(cfg_filename) as f:
  full_config = json.load(f)
  cfg = full_config["data-filtering"]

#########################
# Main                  #
#########################
fileUtils.build_output_directory(output_path)
files = fileUtils.load_files(input_path)

if len(cfg["subjects"]):
  files = fileUtils.filter_files_by_regex(files, fileUtils.build_regex_for_contain_items(cfg["subjects"]))
  if files == None:
    print("No files found under "+input_path)
    exit

if len(cfg["activities"]):
  files = fileUtils.filter_files_by_regex(files, fileUtils.build_regex_for_contain_items(cfg["activities"]))

if len(cfg["trial"]):
  files = fileUtils.filter_files_by_regex(files, fileUtils.build_regex_for_contain_items(cfg["trial"]))

print("\nStarting data-filtering.")
pbar = fileUtils.initialize_progress_bar(len(files))

if len(cfg["columns"]):
  for idx, file in enumerate(files):
    pbar.update(idx)
    new_dataframe = dataFilteringUtils.filter_dataframe_columns(input_path + file, cfg["columns"])
    new_dataframe.to_csv(output_path + file, index=False, float_format='%.8f')
else:
  for idx, file in enumerate(files):
    pbar.update(idx)
    df = pd.read_csv(input_path + file)
    df.to_csv(output_path + file, index=False, float_format='%.8f')

print("\nData-filtering completed.\n")
