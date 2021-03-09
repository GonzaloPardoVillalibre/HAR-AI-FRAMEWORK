from toolz import interleave
import os
import pandas as pd
pd

# Porject main directory path
main_path = os.getcwd()

# Reeds one file from the dataset
file = main_path + '/framework/dataset/S01-Trial-Walk-1.csv'
df = pd.read_fwf(file, header=None)

df = df[0].str.split(',', expand=True)

# Return the first N=15 rows from the data frame for plotting pourposes
# df.head(15)

# Names the columns for the data table with the information indexed in the 5th row
df.columns = df.iloc[5]

# Drops the rows from the data frame with the specified index, as they aren't useful anymore
# (we have already taken the sensor name from the 5th row to the column name).
table = df.drop(axis=0, index=[0, 1, 2, 3, 4, 5])

# Creates list of position sensors to filter in the future via regex.
# Remember each P.S. (position sensor) has 3 values in the dataset.
jointNamesListIMU = ['qBACK', 'RUL', 'RLL',
                     'RLL2', 'RF', 'LUL', 'LLL', 'LLL2', 'LF']

# Creates list of orientation sensors to filter in the future
# Remember, each P.S. has 4 values in the dataset.
jointNamesListVicon = ['qRPV', 'qRTH', 'qRSK',
                       'qRFT', 'qLTH', 'qLSK', 'qLFT']

# The first sensor for the oritentation list is taken to create a data table with only values
# frome this sensor.
jointName = jointNamesListVicon[0]
df = table.filter(regex=jointName+'??')
df.insert(loc=0, column='quat', value=jointName)
# df.head()

# The new data table would look like:
# 5	    quat	qRPV_1	qRPV_2	qRPV_3	qRPV_4
# 6	    qRPV	0.738418036293259	0.0222340202690456	0.0875507545438605	-0.668265903213895
# 7	    qRPV	0.739987260369354	0.0206207535557893	0.085203009706594	-0.66688386256588
# 8	    qRPV	0.741497132672006	0.019305677707201	0.0830403924379386	-0.66551753265501
# 9 	qRPV	0.742979033714284	0.018252393516091	0.0810646884817147	-0.664136674091475
# 10	qRPV	0.744389941328283	0.0174264065971911	0.0792683681009992	-0.662794433758302


##########################
# Approach via functions #
##########################

# Defines the same produce explained above in a funcion for orientation sensors


def extract_quat_columns(file, jointName):
    df = pd.read_fwf(file, header=None)
    df = df[0].str.split(',', expand=True)
    df.columns = df.iloc[5]
    df = df.drop(axis=0, index=[0, 1, 2, 3, 4, 5])
    df = df.filter(regex=jointName+'??')
    df.insert(loc=0, column='quat', value=jointName)
    df.columns = ['quat', '0', '1', '2', '3']
    return df

# Defines the same produce explained above in a funcion for position sensor


def extract_position_columns(file, jointName):
    df = pd.read_fwf(file, header=None)
    df = df[0].str.split(',', expand=True)
    df.columns = df.iloc[5]
    df = df.drop(axis=0, index=[0, 1, 2, 3, 4, 5])
    df = df.filter(regex=jointName+'??')
    df.insert(loc=0, column='3D vecotr', value=jointName)
    df.columns = ['3D vecotr', '0', '1', '2']
    return df

# Example of use:
# Orientation function
# dfqRPV = extract_quat_columns(file, 'qRPV')
# dfqRPV.head()
# Position function
# dfPEL = extract_position_columns(file, 'PEL')
# dfPEL.head()

#########################
# Final aproach         #
#########################


# Cretes a new list. This list will be a list of data frames.
DF_list = list()

# Opens file
subjectAndActivityFile = main_path + '/framework/dataset/S01-Trial-Zigzag-1.csv'

# Creates list for the orientation sensors that will be taken
jointNamesListVicon = ['qRPV', 'qRTH', 'qRSK', 'qRFT', 'qLTH', 'qLSK', 'qLFT']

# For each sensor creates a data frame with all the rows and 4 columns of data each (without indexes)
for item in jointNamesListVicon:
    df = extract_quat_columns(subjectAndActivityFile, item)
    DF_list.append(df.values)

# Interleaves every dataframe in the list. That means, first row of each dataframe, then second, then third...
final_df = pd.DataFrame(interleave(DF_list))
# final_df.head(15)

final_df.to_csv(subjectAndActivityFile[:-4]+'-VICON-AllJoints.csv')

# Saves the new csv with the following data:
#   - Rows: original * number of sensors in the list.
#   - Columns: 4 in orientation sensors, 3 in position.
