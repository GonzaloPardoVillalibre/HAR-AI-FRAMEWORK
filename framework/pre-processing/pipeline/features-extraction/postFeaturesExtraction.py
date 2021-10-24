from toolz import interleave
import os, sys, json, progressbar
import pandas as pd
import featuresExtractionUtils
import shutil

# Current file path
current_path = os.path.dirname(os.path.abspath(__file__))
cfg_filename = current_path + '/../../config.json'

# Path to _output file
output_path = current_path + '/post-segmentation_output/'

# Path to input
input_path = current_path + '/../segmentation/_output/'


# Load file utils file
sys.path.append(current_path + '/../../utils')
import fileUtils

# Loads configuration file
with open(cfg_filename) as f:
  full_config = json.load(f)
  cfg = full_config["pipeline"]["post-features-extraction"]

#########################
# Main                  #
#########################
files = fileUtils.load_files(input_path)

# Prepare output directory
fileUtils.build_output_directory(output_path)

print("\nStarting post-segmentation features extraction.")

if cfg:
  pbar = fileUtils.initialize_progress_bar(len(files))
  for idx, file in enumerate(files):
    pbar.update(idx)
    new_dataframe = featuresExtractionUtils.process(input_path + file, cfg)
    new_dataframe.to_csv(output_path + file, index=False, float_format='%.15f')
else:
  print("Post-segmentation feature extraction empty, copying files to next stage.")
  pbar = fileUtils.initialize_progress_bar(len(files))
  for idx, file in enumerate(files):
      pbar.update(idx)
      shutil.copy(input_path + file, output_path + file)

print("\nPost-segmentation features extraction completed.\n")
