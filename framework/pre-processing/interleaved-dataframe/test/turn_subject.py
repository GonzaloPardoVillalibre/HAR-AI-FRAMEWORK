from toolz import interleave
import os
import pandas as pd
import json
import shutil
import numpy as np
import copy
from scipy.spatial.transform import Rotation as R

main_path = os.getcwd()

file_path = main_path + '/framework/pre-processing/interleaved-dataframe/_output/S08-A09-Orientationjoints-1.csv'
out_path = main_path + '/framework/pre-processing/interleaved-dataframe/test/turn_subject_output.csv'

def unitary_rotation_quaternion(x:float, y:float, z:float, a:float):
  rotation_factor = np.sin( a / 2.0 )
  x = x * rotation_factor
  y = y * rotation_factor
  z = z * rotation_factor
  w = np.cos( a / 2 )
  return [w,x,y,z]

def quaternion_multiply(quaternion1, quaternion0):
    w0, x0, y0, z0 = quaternion0
    w1, x1, y1, z1 = quaternion1
    return np.array([-x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0,
                     x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0,
                     -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0,
                     x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0], dtype=np.float32)

def create_rotated_images(grades, original_df):
  vector_de_rotacion =  unitary_rotation_quaternion(0,0,1, grades*np.pi/180)
  r = R.from_euler('z', 180, degrees=True)
  vector_r = r.as_quat()
  # si usamos este entonces la línea 24 debe ser
  # x0, y0, z0, w0
  # pero si comparamos los dos vemos que el resultado es el mismo.
  original_df_array = original_df.values
  final_df_array = copy.deepcopy(original_df_array)
  i = 0
  for element in original_df_array:
    final_df_array[i] = quaternion_multiply(vector_de_rotacion, element)
    i = i +1
  return final_df_array


#################
#    Main       #
#################
df = pd.read_csv(file_path, header=None)
df = df.iloc[1:]
df_first = df.iloc[:,0].astype(np.float32)
df_first = df_first.reset_index(drop=True)
df = df.drop(df.columns[[0]], axis=1)
df = df.astype(np.float32)
rotated_df = create_rotated_images(180, df)
final_df = pd.DataFrame(rotated_df.reshape(15192,4), columns=["w","x","y","z"])
final_df = pd.concat([df_first, final_df], ignore_index=True, axis=1)
final_df.to_csv(out_path)
