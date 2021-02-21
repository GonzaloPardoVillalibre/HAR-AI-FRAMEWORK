import train
import os, json, gc
import numpy as np
import utils.utils as utils

main_path = os.getcwd()
cfg_files_path = main_path + '/vicon/processing/toTrain'
outcome = main_path + '/vicon/processing/trainOutcomes'
_, _, files = next(os.walk(cfg_files_path))


##########
#  Main  #
##########

for file in files:
    # Clean garbage & load configurations for multiple trains
    gc.collect()
    outcome_path = utils.create_folder(outcome)
    cfg = utils.loadCfgJson(cfg_files_path + '/' + file)

    # Train phase
    model, test_loss, test_accuracy, prediction, history_callback = train.train_main(cfg, outcome_path)

    # Generate report
    utils.save_model_and_weights(outcome_path, model)
    utils.create_confusion_matrix(prediction, outcome_path, cfg["movements"])
    utils.create_outcome_file(outcome_path, model, test_loss, test_accuracy, history_callback)
    utils.create_config_output_file(outcome_path, cfg)
