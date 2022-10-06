################################
# Features extraction Utils    #
################################
import pandas as pd
import numpy as np
import math
#import pyquaternion
def process(file, cfg):
    df = pd.read_csv(file)
    for key, value in cfg.items():
        df = apply_function(key,value, df)
    return df

###############################
# Feature extraction selector #
###############################
def apply_function(function, function_params, df):
    if function == "NormalizedJointAngles":
        return calculate_normalized_joint_angles(df)
    if function == "FFT":
        return calculate_FFT(function_params["combined"], df)
    if function == "converttoradians":
        return convert_to_radians(df)
    if function == "computequatsrootjoint":
        return compute_quats_root_joint(df)

def compute_quats_root_joint():
    #TODO
    return

def convert_to_radians(df):
    for column in df.columns.values:
        df[column] = df[column]*math.pi/180.0
    return df

def calculate_normalized_joint_angles(df):
    joints_range_angle = {"lumbar_extension": (-15,90),
                          "lumbar_bending": (-15,15),
                          "lumbar_rotation": (-90,90),
                          "arm_flex_r": (-30,180),
                          "arm_add_r": (-90,90),
                          "arm_rot_r": (-90,90),
                          "elbow_flex_r": (0,90),
                          "pro_sup_r": (-30,30),
                          "arm_flex_l": (-30,180),
                          "arm_add_l": (-90,90),
                          "arm_rot_l": (-90,90),
                          "elbow_flex_l": (0,90),
                          "pro_sup_l": (-90,90),
                          }
    for column in df.columns.values:
        min = joints_range_angle[column][0]
        max = joints_range_angle[column][1]
        df[column] = df[column]/90.0#(max-min)
    return df


def calculate_FFT(combined, df):
    names = df.columns.values.tolist()
    nameRealFFT = ['RFFT-' + name for name in names]
    nameimaginaryFFT = ['IFFT-' + name for name in names]
    data = df.values
    data = data.astype(np.float32)
    data = np.fft.fft2(data).round(15)
    fft_df_real = pd.DataFrame(data.real.astype(np.float32), columns=nameRealFFT)
    fft_df_imag = pd.DataFrame(data.imag.astype(np.float32), columns=nameimaginaryFFT)
    if combined:
        return pd.concat([df, fft_df_real, fft_df_imag], axis=1)
    else:
        return pd.concat([fft_df_real, fft_df_imag], axis=1)
