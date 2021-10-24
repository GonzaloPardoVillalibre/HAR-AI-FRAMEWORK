from toolz import interleave
import os, sys, json, progressbar
import pandas as pd
import dataAugmentationUtils
import shutil

# Current file path
current_path = os.path.dirname(os.path.abspath(__file__))
cfg_filename = current_path + '/../../config.json'

# Path to _output file
output_path = current_path + '/_output/'

# Path to input
input_path = current_path + '/../data-filtering/_output/'


# Load file utils file
sys.path.append(current_path + '/../../utils')
import fileUtils

# Loads configuration file
with open(cfg_filename) as f:
  full_config = json.load(f)
  cfg = full_config["pipeline"]["data-augmentation"]

#########################
# Main                  #
#########################
files = fileUtils.load_files(input_path)

# Prepare output directory
fileUtils.build_output_directory(output_path)

print("\nStarting data augmentation.")

if len(cfg["rotationGradesList"]) and (len(cfg["4D-Sensors"]) or len(cfg["3D-Sensors"])):
  pbar = fileUtils.initialize_progress_bar(len(files))
  for idx, file in enumerate(files):
      pbar.update(idx)
      dataAugmentationUtils.augmentData(input_path, output_path, file, cfg["rotationGradesList"], cfg["4D-Sensors"], cfg["3D-Sensors"])
else:
  print("Data augmentation disabled, copying files to next stage.")
  pbar = fileUtils.initialize_progress_bar(len(files))
  for idx, file in enumerate(files):
      pbar.update(idx)
      shutil.copy(input_path + file, output_path + str(file[:-4]) +'-0°.csv')

print("\nData augmentation completed.\n")

if full_config["pipeline"]["detele-previous-output-directory"]:
  fileUtils.removeInputDirectory(input_path)