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

def extract_by_quat(df,quat):
    dfnew = df[df['QUAT'] == quat]
    dfnew = dfnew.drop('timestamp',axis=1)
    dfnew.reset_index(drop=True, inplace=True)
    column_names = dfnew.columns.to_list()
    #print(column_names)
    new_column_names = []
    joint = column_names[0]
    for i,column in enumerate(column_names):
        if i==0:
            new_column_names.append(quat)
        if i>0:
            #print(joint+"_"+column)
            new_column_names.append(quat+"_"+column)
    #print(new_column_names)
    dfnew.columns=new_column_names
    #dfnew.head()
    return dfnew

def process_raw_file(dfraw):
    #REMOVE FIRST LINES OF QUATS (CALIBRATION ORIENTATION where timestamp == 0)
    dfraw = dfraw[dfraw.timestamp > 0]
    quats = dfraw['QUAT'].unique()   #quat names
    dflist = []
    for quat in quats:
        dfnew = extract_by_quat(dfraw,quat)
        dflist.append(dfnew)
    dfconcat = dflist[0]
    for i,df in enumerate(dflist):
        if i>0:
            dfconcat=pd.concat([dfconcat,df],axis=1)
    #REMOVE columns with quat names
    dfconcat=dfconcat.drop(columns=quats)
    return dfconcat

for dir in dirs:
    if dir[0]=='A': 
        #DATA ORGANIZED IN ACTIVITIES
        for file in os.listdir(os.path.join(input_folder,dir)):
            extension = file[len(file)-4:]
            print(file)

            if extension == '.raw':
                print(input_folder+'/'+file)
                dfraw = pd.read_csv(os.path.join(input_folder,dir,file),sep=',')
                dfnew = process_raw_file(dfraw)
                #New filename
                filname = file.replace("_","-")
                if "S01" in file:
                    #Change T02 to T01 for that subject
                    filname = filname.replace("T02","T01")
                #filname = filname.replace("T0","")
                filname = filname.replace(".raw",".csv")
                dfnew.to_csv(output_file + filname, index=False)
                
            
            
            
