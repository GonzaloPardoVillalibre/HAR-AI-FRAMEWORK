from toolz import interleave
import os
import pandas as pd
import json
import shutil 

# Porject main directory path
main_path = os.getcwd()
# main_path = '/TFG'

input_folder = main_path +  '/framework/pre-processing/tunning-examples/Harvard-tunning-example/original-dataset'
_, _, files = next(os.walk(input_folder))
output_file = main_path +  '/framework/pre-processing/tunning-examples/Harvard-tunning-example/framework-input-dataset/'

files.remove('.gitkeep')

for file in files:
    df = pd.read_csv(input_folder + '/' + file, header=None, skiprows=[0,1,2,3,4], low_memory=False)
    column_names = df.iloc[0].values
    df = df.iloc[1:]
    df.columns = column_names
    filname = file.replace("-Trial", "")
    df.to_csv(output_file + filname, index=False)
    print(file)
