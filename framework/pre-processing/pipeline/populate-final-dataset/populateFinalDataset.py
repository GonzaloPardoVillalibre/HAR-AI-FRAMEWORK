from toolz import interleave
import os, sys, json, progressbar
import pandas as pd
import shutil

# Current file path
current_path = os.path.dirname(os.path.abspath(__file__))
cfg_filename = current_path + '/../../config.json'

# Path to _output file
output_path = current_path + '/../../../final-dataset/'

# Path to input
input_path = current_path + '/../features-extraction/post-segmentation_output/'

# Load file utils file
sys.path.append(current_path + '/../../utils')
import fileUtils

# Loads configuration file
with open(cfg_filename) as f:
  full_config = json.load(f)
  cfg = full_config["pipeline"]["populate-final-dataset"]

#########################
# Main                  #
#########################
files = fileUtils.load_files(input_path)

if cfg["clean-before"]:
    fileUtils.build_output_directory(output_path)
    open(output_path + '.gitkeep', 'w')

print("\nStarting final dataset population.")
pbar = fileUtils.initialize_progress_bar(len(files))

for idx, file in enumerate(files):
    pbar.update(idx)
    shutil.copy(input_path + file, output_path)

print("\nFinal dataset population completed.\n")

if full_config["pipeline"]["detele-previous-output-directory"]:
  fileUtils.removeInputDirectory(input_path)