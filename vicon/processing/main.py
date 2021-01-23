import utils.utils as utils
import re, os, json

main_path = os.getcwd()
final_input_path = main_path + '/vicon/pre-processing/final-dataset/orientation/'
cfg_filename = main_path + '/vicon/processing/config.json'

with open(cfg_filename) as f:
  cfg = json.load(f)

_, _, files = next(os.walk(final_input_path))
##########
#  Main  #
##########

train_set, validation_set, test_set = utils.split_dataset(files, cfg)

