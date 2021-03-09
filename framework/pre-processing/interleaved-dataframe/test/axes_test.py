from toolz import interleave
import os
import pandas as pd
import json
import shutil     
import numpy as np
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/gonzalo/Documents/TFG/framework/pre-processing/interleaved-dataframe/test/axes_test.csv", header=None)
first_colum = df.iloc[:,2].values
second_colum = df.iloc[:,3].values
third_colum = df.iloc[:,4].values

# norm_uno = np.linalg.norm(first_colum)
# var_uno = (first_colum/norm_uno).var()
# min_uno = first_colum.min()
# max_uno = first_colum.max()
# diff_uno = max_uno - min_uno
# adiff_normed_uno = diff_uno / norm_uno

# norm_dos = np.linalg.norm(second_colum)
# var_dos = (second_colum/norm_dos).var()
# min_dos = second_colum.min()
# max_dos = second_colum.max()
# diff_dos = max_dos - min_dos
# adiff_normed_dos = diff_dos / norm_dos

# norm_tres = np.linalg.norm(third_colum)
# var_tres = (third_colum/norm_tres).var()
# min_tres = third_colum.min()
# max_tres = third_colum.max()
# diff_tres = max_tres - min_tres
# adiff_normed_tres = diff_tres / norm_tres

plt.figure(0)
plt.plot(first_colum)

plt.figure(1)
plt.plot(second_colum)

plt.figure(2)
plt.plot(third_colum)

plt.show()
# orig_uno = first_colum.var()
# orig_dos = second_colum.var()
# orig_tres = third_colum.var()
print("Fin prueba")
