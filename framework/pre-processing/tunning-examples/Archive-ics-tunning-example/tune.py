from toolz import interleave
import os
import pandas as pd
import json
import shutil 

# Porject main directory path
main_path = os.getcwd()
# main_path = '/TFG'

input_folder = main_path +  '/framework/pre-processing/tunning-examples/Archive-ics-tunning-example/original-dataset'
_, _, files = next(os.walk(input_folder))
output_file = main_path +  '/framework/pre-processing/tunning-examples/Archive-ics-tunning-example/framework-input-dataset/'
files.remove('.gitkeep')

column_names = ['RLA_1', 'RLA_2', 'RLA_3', 'RLA_4', 
         'RUA_1', 'RUA_2', 'RUA_3', 'RUA_4', 
         'BACK_1', 'BACK_2', 'BACK_3', 'BACK_4', 
         'LUA_1', 'LUA_2', 'LUA_3', 'LUA_4',
         'LLA_1', 'LLA_2', 'LLA_3', 'LLA_4',
         'RC_1', 'RC_2', 'RC_3', 'RC_4',
         'RT_1', 'RT_2', 'RT_3', 'RT_4',
         'LT_1', 'LT_2', 'LT_3', 'LT_4',
         'LC_1', 'LC_2', 'LC_3', 'LC_4']

activities ={ 1:'A01', 2:'A02', 3:'A03', 4:'A04', 5:'A05', 6:'A06', 7:'A07', 8:'A08', 9:'A09', 10: 'A10',  
              11: 'A11', 12: 'A12', 13: 'A13', 14: 'A14', 15: 'A15', 16: 'A16', 17: 'A17', 18: 'A18', 19: 'A19', 20: 'A20',
              21: 'A21', 22: 'A22', 23: 'A23', 24: 'A24', 25: 'A25', 26: 'A26', 27: 'A27', 28: 'A28', 29: 'A29', 30: 'A30', 31:'A31', 32: 'A32', 33: 'A33'              
    }

for file in files:
    df = pd.read_csv(input_folder+ '/' + file, header=None, sep="\t")
    subject = file.split("_")[0].replace("subject", "")
    if int(subject)<10:
        subject = 'S0' + subject
    else:
        subject = 'S' + subject
    
    for i in range(1,34):
        i_df = df.loc[ ( df.iloc[:,-1] == i)]
        i_df = i_df.iloc[:, [11,12,13,14,24,25,26,27,37,38,39,40,50,51,52,53,63,64,65,66,76,77,78,79,89,90,91,92,102,103,104,105,115,116,117,118]]
        i_df = i_df.astype('float32')
        i_df.columns = column_names
        final_df_values = i_df.values
        if 'ideal' in file:
            i_df.to_csv(output_file + subject + '-' + activities[i] + '-1.csv', index=False)
        elif 'mutual' in file:
            i_df.to_csv(output_file + subject + '-' + activities[i] + '-2.csv', index=False)
        else:
            i_df.to_csv(output_file + subject + '-' + activities[i] + '-3.csv', index=False)
    print(file)
