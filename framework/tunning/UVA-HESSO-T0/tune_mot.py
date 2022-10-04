from toolz import interleave
import os
import pandas as pd
import json
import shutil 

# Current directory
current_path = os.path.dirname(os.path.abspath(__file__))

input_folder = current_path+  '/original-dataset'
root, dirs, files = next(os.walk(input_folder))
output_file = current_path +  '/../../pre-process/dataset/'

for dir in dirs:
    if dir[0]=='A': 
        #DATA ORGANIZED IN ACTIVITIES
        for file in os.listdir(os.path.join(input_folder,dir)):
            extension = file[len(file)-4:]
            print(file)

            if extension == '.mot':
                print(input_folder+'/'+file)
                dfmot = pd.read_csv(os.path.join(input_folder,dir,file),skiprows=6,sep='\t')
                #Remove calibration frame
                dfmot = dfmot.iloc[1:]
                #New filename

                filname = file.replace("ik_", "")
                filname = filname.replace("_","-")
                if "S01" in file:
                    #Change T02 to T01 for that subject
                    filname = filname.replace("T02","T01")
                #filname = filname.replace("T0","")
                filname = filname.replace(".mot",".csv")
                dfmot.to_csv(output_file + filname, index=False)
                
            
            
            
