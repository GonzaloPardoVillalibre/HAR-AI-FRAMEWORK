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

def expandcolumn(df,imu):
    dfquat = df[imu].str.split(',',4,expand=True)
    dfquat.columns=[imu+"_w",imu+"_x",imu+"_y",imu+"_z"]
    return dfquat

def process_sto_file(dfraw):
    #REMOVE FIRST LINES OF QUATS (CALIBRATION ORIENTATION where timestamp == 0)
    dfraw = dfraw[dfraw.time > 0]
    dfraw.pop('time')
    dflist = []
    imus = dfraw.columns.to_list()
    for imu in imus:
        dfquat = expandcolumn(dfraw,imu)
        dflist.append(dfquat)
    dfconcat = dflist[0]
    for i,df in enumerate(dflist):
        if i>0:
            dfconcat=pd.concat([dfconcat,df],axis=1)
    return dfconcat

for dir in dirs:
    if dir[0]=='A': 
        #DATA ORGANIZED IN ACTIVITIES
        for file in os.listdir(os.path.join(input_folder,dir)):
            extension = file[len(file)-4:]
            print(file)

            if extension == '.sto':
                print(input_folder+'/'+file)
                dfraw = pd.read_csv(os.path.join(input_folder,dir,file),sep='\t',skiprows=5)
                dfnew = process_sto_file(dfraw)
                #New filename
                filname = file.replace("_","-")
                if "S01" in file:
                    #Change T02 to T01 for that subject
                    filname = filname.replace("T02","T01")
                #filname = filname.replace("T0","")
                filname = filname.replace(".sto",".csv")
                dfnew.to_csv(output_file + filname, index=False)
                
            
            
            
