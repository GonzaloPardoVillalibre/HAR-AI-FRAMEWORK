############################
# Data Augmentation Utils  #
############################
import numpy as np
from numpy.lib.function_base import _calculate_shapes 
import pandas as pd
import copy

def augmentData(input_path, output_path, file:str, rotationGradesList:list, FourDSensors:list, ThreeDSensors:list):
    df = pd.read_csv(input_path + file)
    for rotationGrades in rotationGradesList:
        dataframe = copy.deepcopy(df)
        if len(FourDSensors):
            rotate4DSensors(rotationGrades, dataframe, FourDSensors)
        # if len(ThreeDSensors): --> TO DO 
        dataframe.to_csv(output_path + str(file[:-4]) +'-' + str(rotationGrades) + "°" + '.csv', index=False, float_format='%.15f')

def rotate4DSensors(grades,df, sensorNames):
    unitaryRotationVector =  unitary_rotation_quaternion(0,0,1, grades*np.pi/180)
    [rotate4DSensor(unitaryRotationVector, df, sensorName) for sensorName in sensorNames]
    return df

def unitary_rotation_quaternion(x:float, y:float, z:float, a:float):
    rotation_factor = np.sin( a / 2.0 )
    x = x * rotation_factor
    y = y * rotation_factor
    z = z * rotation_factor
    w = np.cos( a / 2 )
    return [w,x,y,z]

def rotate4DSensor(unitaryRotationVector,df, sensorName):
    w1, x1, y1, z1 = unitaryRotationVector
    w0 = df[sensorName+"_1"]
    x0 = df[sensorName+"_2"]
    y0 = df[sensorName+"_3"]
    z0 = df[sensorName+"_4"]
    w = -x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0
    x = x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0
    y = -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0
    z = x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0
    df[sensorName+"_1"] = w 
    df[sensorName+"_2"] = x 
    df[sensorName+"_3"] = y
    df[sensorName+"_4"] = z
