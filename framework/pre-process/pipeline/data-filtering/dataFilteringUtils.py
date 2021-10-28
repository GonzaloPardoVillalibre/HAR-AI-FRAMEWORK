#########################
# Data Filtering Utils  #
#########################
import os, sys
# Current file path
current_path = os.path.dirname(os.path.abspath(__file__))
# Load file utils file
sys.path.append(current_path + '/../../utils')
import dataframeUtils
import pandas as pd

# Remain only with the desired columns from the dataframes
def filter_dataframe_columns(file:str, columns:list):
    df = pd.read_csv(file)
    df = df.filter(items=columns)
    return df