from toolz import interleave
import os
import pandas as pd
import json
import shutil 
import re
from pyquaternion import Quaternion
import numpy as np
from scipy.spatial.transform import Rotation as R

# Current directory
current_path = os.path.dirname(os.path.abspath(__file__))
#current_path = '/framework/tunning/Archive-ics-tunning-example'
output_folder = current_path + '/../../pre-process/dataset'


input_folder = current_path +  '/original-dataset'
_, _, files = next(os.walk(input_folder))
calibration_folder = current_path +  '/calibration'
_, _, calib_files = next(os.walk(calibration_folder))
files.remove('.gitkeep')

# imuBack = Quaternion([ 0.6845527, 0.05967249, 0.7225831, -0.0755007])
# imuBack =Quaternion([0.05967249,  0.72258314, -0.0755007,   0.68455274])
# inst_BACK = Quaternion([ -0.3, -0.7, -0.4, 0.5])
# imuBack =Quaternion([0.68, 0.05, 0.72, -0.07])
# imuBack_inverse = imuBack.inverse
# result1 = inst_BACK * imuBack_inverse

# inst_BACK =  R.from_quat([ -0.3, -0.7, -0.4, 0.5])
# imuBack = R.from_quat([0.68, 0.05, 0.72, -0.07])
# imuBack_inverse = imuBack.inv()
# result2= inst_BACK * imuBack_inverse


###################
# Add calibration #
###################
def calibrate_activities(i_df, subject):
    user_regex_string ="^"+subject+"-"
    calib_file = [val for val in calib_files if re.search(user_regex_string, val)][0]

    if not calib_file:
        return

    calib_df = pd.read_csv(calibration_folder + '/' + calib_file, header=None)
    sensors= calib_df[0].to_list()
    calib_df = calib_df.drop(calib_df.columns[[0]], axis=1)
    calib_values = calib_df.values

    for i in range(len(calib_values)):
        sensor_name = sensors[i]
        calib_vector = calib_values[i]
        qv = Quaternion(calib_vector)
        qv_inverted = qv.inverse
        for index, row in i_df.iterrows():
            if sensor_name + "_1" in row:
                vector = Quaternion([row[sensor_name + "_1"], row[sensor_name + "_2"],row[sensor_name + "_3"],row[sensor_name + "_4"]])
                final_vector = vector * qv_inverted 
                row[sensor_name + "_1"] = final_vector.w
                row[sensor_name + "_2"] = final_vector.x
                row[sensor_name + "_3"] = final_vector.y
                row[sensor_name + "_4"] = final_vector.z

###################
# Extract sensors #
###################

column_names = ['ACC_X','ACC_Y','ACC_Z','RLA_1', 'RLA_2', 'RLA_3', 'RLA_4', 
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
    if 'ideal' in file:
        df = pd.read_csv(input_folder+ '/' + file, header=None, sep="\t")
        subject = file.split("_")[0].replace("subject", "")
        if int(subject)<10:
            subject = 'S0' + subject
        else:
            subject = 'S' + subject
        
        for i in range(9,34):
            i_df = df.loc[ ( df.iloc[:,-1] == i)]
            i_df = i_df.iloc[:, [2,3,4,11,12,13,14,24,25,26,27,37,38,39,40,50,51,52,53,63,64,65,66,76,77,78,79,89,90,91,92,102,103,104,105,115,116,117,118]]
            i_df = i_df.astype('float32')
            i_df.columns = column_names
            calibrate_activities(i_df, subject)
            final_df_values = i_df.values
            if 'ideal' in file:
                i_df.to_csv(output_folder + '/' + subject + '-' + activities[i] + '-1.csv', index=False)
            elif 'mutual' in file:
                i_df.to_csv(output_folder + '/' + subject + '-' + activities[i] + '-2.csv', index=False)
            else:
                i_df.to_csv(output_folder + '/' + subject + '-' + activities[i] + '-3.csv', index=False)
        print(file)
