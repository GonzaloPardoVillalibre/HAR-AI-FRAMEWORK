################################
# Features extraction Utils    #
################################
import pandas as pd
import numpy as np
def process(file, cfg):
    df = pd.read_csv(file)
    for key, value in cfg.items():
        df = apply_function(key,value, df)
    return df

###############################
# Feature extraction selector #
###############################
def apply_function(function, function_params, df):
    if function == "FFT":
        return calculate_FFT(function_params["combined"], df)

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
