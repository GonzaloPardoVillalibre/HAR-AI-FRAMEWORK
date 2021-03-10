-----------------------------------------

# Pre-processing environment
This environment represents the most specific utility of the framework and it is designed to preprocess time series datasets of ***quaternions*** or ***3D vectors***; such, for example, those obtained while measuring any type of movement with sensors on a certain subject. To ensure your dataset fits the requirements, make sure to have a look at the **input dataset format** section.

If you want to know more about quaternions: https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation

## Input dataset format: 
As said, if your original dataset does not contain such type of data, this environment may not fit your necessities. How must be my dataset then if I want to use this environment? These are the requirements:

Dataframes (as .csv files) from N subjects performing different activities. Each dataframe must have the following format:
- **Rows must represent timesteps**, that means, one instant per row.
- **Colums must represent sensor's information**.
    - **Position sensors**

      Given a 3D sensor called "KNEE", position sensors columns must be named [KNEE_1, KNEE_2, KNEE_3]. A graphic example can be found here:  [position dataframe example](doc/images/3d_vector_input_dataset.png)

    - **Orientatin sensors**

      Given a Quaternion sensor called "LFOOT", orientation sensor columns must be named [LFOOT_1, LFOOT_2, LFOOT_3, LFOOT_4]. A graphic example can be found here:  [orientation dataframe example](doc/images/quaternion_input_dataset.png)

Some datasets examples could be:

- https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/9QDD5J (Harvard dataset)
- https://archive.ics.uci.edu/ml/datasets/REALDISP+Activity+Recognition+Dataset (Archive-ics dataset)

**Important recall:** these are the minimum format requirements in terms of data information. Although, to make use of the environment you might have to tune the naming of your files or make other small changes. Theere is also two tunnning examples for the already mentioned dataset.

- [Harvard-tunning-example](tunning-examples/Harvard-tunning-example)
- [Archive-ics-tunning-example](tunning-examples/Archive-ics-tunning-example)

**Do not panic, specific format requirements for each module will be detailed along this guide.**
## General transformation


TO DO


## Environment architecture

![Usage_schema](doc/images/pre-processing-environment-architecture.png)

The architecture is composed from 4 pseudo-independent modules:

- Interleaved dataframe
- Image builder
- Image enricher
- Final dataset


### Composed interleaved dataframes
According to the information recorded by the sensors there will be `two` types of composed dataframes; one for `orientation` data (four inputs per row); and another one for `position` data (three inputs per row). Pre -processing of each type can be enabled via `config.json` and composed-dataframes csv will be named using the `subject` number (1-10), `movement` or activity, `sample` number (1-2) and dataframe type.

``` 
    Subject-Movement-Orientationjoints-Samplenumber.csv
    Subject-Movement-Positionjoints-Samplenumber.csv
```

#### Orientation dataframes

+ #### Build individual dataframes per sensor
    Choosing at least one element from the available orientation sensor list:
    ```
     ["qRPV", "qRTH", "qRSK", "qRFT", "qLTH", "qLSK", "qLFT"]
    ```
    The script will build its individual dataframe. p.e. (qRPV):
    
    ![Usage_schema](../doc/images/individual-orientation-df.png)
    
+ #### Build composed & interleaved dataframe for a certain activity and subject:
    
    For every sensor chosen beforewards, the script will interleave its dataframes. p.e. (qRPV, qRTH & qRSK) : 

    ![Usage_schema](../doc/images/composed-orientation-df.png)
    

#### Positon dataframes

+ #### Build individual dataframes per sensor
    Choosing at least one element from the available position sensor list:
    ```
     ["LTOE", "PELV", "RFEP", "LFEP", "RFEO", "LFEO", "RTIO", "LTIO"]
    ```
    The script will build its individual dataframe. p.e. (LTOE):
    
    ![Usage_schema](../doc/images/individual-position-df.png)

+ #### Build composed & interleaved dataframe for a certain activity and subject:

    For every sensor chosen beforewards, the script will interleave its dataframes. p.e. (LTOE, PELV & RFEP) : 

    ![Usage_schema](../doc/images/composed-position-df.png)
