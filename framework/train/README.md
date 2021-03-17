-----------------------------------------

# Training environment
This environment represents the most general and useful utility of the framework and it is designed to train several types of neural networks such CNN or RNN **when the dataset is conformed by .csv files, where each .csv represents itself a sample and the name of the file discribes the label for that sample**. Therefore, the naming of the .csv files is critical and will be reviewed in detail in the ***Input dataset format*** section.

This environment also provides a set of tools to automatically perform trainings varying parameters such:

- Which files conform the training, test and validation datasets.
- Which model is going to be used.
- Which hyperparemeters are beeing used.
- Perform K-fold trainings for multiple subjects.

Finally, it also provides several tools to generate reports after the training process such **performance metrics** or **confusion matrices**.

For the reference, this document includes the following sections:
- Input dataset format.
- Environment architecture & performance.
- Usage guide & configuration file.

## Input dataset format: 
As mentioned, **.CSV files naming** is the key for this environment and must follow this rule:
`**subject(?)activity(?)-authenticity.csv**`:
    
- **subject**: name of the subject performing the activity. Each subject name must be unique and cannot be a substring of another subject name. Watch out the first point of ***CAN I STILL USE THIS FRAMEWORK IF...*** section if you don't have subjects.
- **activity**: label for the activity. Each activity label must be unique and cannot be a substring of other activity label.Watch out the second point of ***CAN I STILL USE THIS FRAMEWORK IF...*** section if you don't have activities.
- **authenticity**: identifier to specify whether the .csv proceedes from a original sample or is a result of any kind of augmentation. This is **very important**, as non original files will not be taken into account for validation and tests datasets. Watch out the third point of ***CAN I STILL USE THIS FRAMEWORK IF...*** section if you don't have subjects.

    - 0: If the .csv file comes from an original sample.
    - Not 0 if it comes from any type of augmentation.
        
**Important recall:** (?) marks mean any type if string can be inbetween.

Some valid .csv names could be:
- **S01-A09-Orientationjoints-1-1-45.csv**
    - Subject: S01
    - Activity: A09 
    - Authenticity: not original, equals it comes from data augmentation.
    - Random strings inbetween: -Orientationjoints-1-1
- **S01-A09-Orientationjoints-1-1-0.csv**
    - Subject: S01
    - Activity: A09 
    - Authenticity: original
    - Random string inbetween: -Orientationjoints-1-1
- **S09-HighKneeJog-Orientationjoints-2-40-0.csv**
    - Subject: S09
    - Activity: HighKneeJog 
    - Authenticity: original
    - Random string inbetween: -Orientationjoints-2-40

### CAN I STILL USE THIS FRAMEWORK IF...
`... I dont have multiple subjects?`
Yes, but you  have to tune your data as validation, test and traing datasets split is made via this tag. Eg:

- Train subjects: S01, S02, S03 (only files from this subjects are taken for training).
- Test subjects: S04 (only files from this subjects are taken for testing).
- Validation subjects: S05 (only files from this subjects are taken for validation).
    
For this case you want to have as much "fictional subjects" as posible to have the minnor variance in results as you change one subject from one group to another.

`... I don't have activities but something else?`
Yes, labeling is not reduced to activities but can be anything from potatoes to economical results for example.

`... I only have original data?`
Then all your files must end with ***-0.csv*** 

## Environment architecture & performance

![Usage_schema](doc/images/pre-processing-environment-architecture.png)

As detailed earlier, this environment is intended to work with time-series dataframes build, either from **position** (3D) or **orientation** (quaternions) sensors. The architecture is composed from 4 pseudo-independent modules, and each one performs a specific pre-processing operation; those layers are:

- Interleaved dataframe
- Image builder & image enricher
- Final dataset


### Interleaved dataframe 

Input dataframes/.csv can contain only 3D sensors information, only orientation sensors, or both. As orientation and position sensors will be treated independently for now on, this module will split position data and orientation data from the input files.

Given an input file called `S01-Walk-1.csv` containing both orientation and position sensors the graphical example of this transformation will be:

![Usage_schema](doc/images/Interleaved_dataframe_split.png)

As represented two new files will be generated:

- `S01-Walk-Positionjoints-1.csv`: contains only position sensors data.
- `S01-Walk-Orientationjoints-1.csv`: contains only orientation sensors data.

The second operation of this module may be irrelevant to the general use as it provides an easy way to tune the data for representing the movement in a Unity framework. This may be useful to check whether any sensor has corrupted data. 

Given one dataframe/.csv called `S01-Walk-Positionjoints-1.csv` (only from position sensors) this is a graphical example for this second transformation:

![Usage_schema](doc/images/Interleaved_dataframe.png)

### Image builder & image enricher

This both modules recover the previous non-unity format and slice the dataframes in windows of **N time-steps** to fit the neural network, for the reference we will call them ***images***. That means, each .csv/dataframe will create a vast number of images. 

Given one original dataframe compound from position sensors, the subject with name ***S01*** and activity ***walk***; this is a graphical example of the image building process with size **5** time-steps:

![Usage_schema](doc/images/Image_builder.png)


Overlap between images can also be configured (given the same example with **2** steps overlap):


![Usage_schema](doc/images/Image_builder_overlap.png)


This transformation is made in two steps: 
- 1- **Image builder**: taking the unity compatible format dataframes from the previous layer (interleaved dataframe) the utility builds multiple images with sizes:
    - **rows**: n-timeSteps * numberOfSensors.
    - **columns**: 3 columns if position sensors are used 4 if orientation sensors are used.
 
    This allows the developer to test each image in unity. The output of this step is not represented, but will be stored in `framework/pre-processing/image-builder/_output`

- 2- **Image enricher**: this utility resizes each image output from the *image builder* with sizes:
    - **rows**: n-timeSteps.
    - **columns**: 3 * numberOfSensors if position sensors are used 4 * numberOfSensors if orientation sensors are used.
 
    The output will be alike the one represented upwards.

But this is not everything yet, the ***image enricher*** module can perform another two optional operations:
- **Data augmentation**: this operation is exclusive for ***Orientationjoints*** images. 

    For a list of grades to rotate (see reference in ***Usage guide & configuration file*** section) this step will rotate each quaternion over the Z axis (assuming this is the vertical axis) and save the output in a newer image.
    
    This means, from a hypothetical image called `S01-Walk-Orientationjoints-1-1.csv` and a list of [0,90,180] three new images will be generated:

    - `S01-Walk-Orientationjoints-1-1-0.csv` (no rotation actually).
    - `S01-Walk-Orientationjoints-1-1-90.csv` (90º grade rotation round vertical axis).
    - `S01-Walk-Orientationjoints-1-1-180.csv` (180º grade rotation round vertical axis).



- **2D FFT calculation**:  this operation can be performed for both types of images.
    
    The 2D fast Fourier Transform is calculated for each image, then the value is split in two matrices, one for real and another one for imaginary values. It is optional to save the image without the 2D FFT, save only the 2D FTT new matrices or horizontally concatenate those matrices to the initial image.
    
    This is a graphical example for this very last option:

    ![Usage_schema](doc/images/2DFFT.png)



### Final dataset

This is the very last module of this environment, its unique function is to move the output from the ***image enricher*** to the shared volume ***"final-dataset"***. Activities can be filtered here.


## Usage guide & configuration file
Once you enter the preprocess environment, you can use `make` to perform the following operations:
```
Usage: make <command>
Commands:
  help:                                  Show this help information
  build-interleaved-dataframes           Excute interleaved dataframe script.
  build-images                           Excute image builder script.
  enrich-images                          Excute image enricher script.
  build-final-dataset                    Excute final dataset script.
  build-all:                             Execute all preprocessing steps by order.

Usual order:
  1. build-interleaved-dataframes
  2. build-images
  3. enrich-images
  4. build-final-dataset
```

But the real key of this environment is the vast amount of configurable parameters. This is done via the `framework/pre-processing/config.json` and should also be adapted for every different dataset. Also a preprocessing environment configuration file is included for the two already mentioned datasets:
- ![Harvard dataset pre-process config file example](tunning-examples/Harvard-tunning-example/framework-config-example.json)
- ![Archive-ics dataset pre-process config file exmple](tunning-examples/Archive-ics-tunning-example/framework-config-sergio.json)

**Reminder**: the name and path for the configuration file must always be ![framework/pre-processing/config.json](config.json)

The following tables will detail the confiragution parameters for each module: 

### Interleaved dataframe 
Fields inside `in-dt` block in `config.json`

| Field | Type | Description |
| -------- |--------- | ----------- |
| enabled  | boolean | Enables interleaved dataframe script execution. |
| subjects.list  | `Array<String>`| List of subjects to include in preprocess. |
| movements.list |`Array<String>` |  List of activities to include in preprocess. |
| movements.samples | `Array<String>` | List of trials to include in preprocess. |
| orientationSensors.enabled   | boolean | Enables orientation sensors processing. |
| orientationSensors.list | `Array<String>`  |  List of orientation sensors to include in preprocess. |
| position.enabled   | boolean | Enables position sensors processing. |
| position.list | `Array<String>` |  List of position sensors to include in preprocess. |

**Disclaimer**: fields such ***movements.list*** or ***sensors lists*** will have impact in other modules too.

### Image builder 
Fields inside `image-builder` block in `config.json`

| Field | Type | Description |
| -------- |--------- | ----------- |
| enabled  | boolean | Enables image builder script execution. |
| orientationSensors.enabled   | boolean | Enables orientation sensors processing. |
| positionSensors.enabled   | boolean | Enables position sensors processing. |
| images.window-size | int |  Time-steps per image. |
| images.overlap | int |  Time-steps shared with previous image. |
| deletePrevious | boolean | deletes output folder from the interleaved dataframe module. |

### Image enricher
Fields inside `image-enricher` block in `config.json`

| Field | Type | Description |
| -------- |--------- | ----------- |
| deepen-images   | boolean | Enables image enricher script execution. |
| table-images   | boolean | DRAFT: Enables table-images script execution. |
| dataAugmentationRotation.gradeList | `Array<Int>` | List of grades to perform data augmentation via rotation.**\*** |
| FFT.enabled | boolean | Enables 2D FFT calcuation. |
| FFT.combined | boolean | Enables combination of the initial image with the 2D FFT output. |
| FFT.saveWithoutFFT | boolean |  To save the initial image without the 2D FFT or not. |
| deletePrevious | boolean | deletes output folder from the interleaved dataframe module. |

**\***  "gradeList":[0] will mean no rotation is done.

### Final dataset
Fields inside `final-dataset` block in `config.json`

| Field | Type | Description |
| -------- |--------- | ----------- |
| movements.list | `Array<String>` |  List of activities to include in preprocess. |
| FFT-input | `Array<Int>` | In case **FFT.combined** and **FFT-saveWithOutFFT** are both enabled this will select which image-enricher output propagate to the shared folder.|

