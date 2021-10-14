from toolz import interleave
import os
import pandas as pd
import json
import shutil 

# Current directory
current_path = os.path.dirname(os.path.abspath(__file__))

input_folder = current_path+  '/original-dataset'
_, _, files = next(os.walk(input_folder))
output_file = current_path +  '/../../pre-processing/dataset/'

files.remove('.gitkeep')

for file in files:
    df = pd.read_csv(input_folder + '/' + file, header=None, skiprows=[0,1,2,3,4], low_memory=False)
    column_names = df.iloc[0].values
    df = df.iloc[1:]
    df.columns = column_names
    filname = file.replace("-Trial", "")
    df.to_csv(output_file + filname, index=False)
    print(file)
