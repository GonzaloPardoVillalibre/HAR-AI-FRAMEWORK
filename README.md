-----------------------------------------

# Gonzalo Pardo's final degree project

-----------------------------------------

## Use of neural networks in human activities classification

This project is the final assignment for Gonzalo Pardo Villalibre. The aim will be to detect which activity is doing a certain subject, minimizing the number of sensors needed. Therefore the student will take advantage of the use of con NN (neural networks) of different types such as CN (convolutional networks) or RN (recurrent networks).

The data set will be taken from https://dataverse.harvard.edu/. Named as `Replication Data for Estimating Lower Limb Kinematics using a Reduced Wearable Sensor Count` this data set contains information from **9 totally healthy subjects** performing different activities meassured by two systems: **Vicon & Xsens**.

Download: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/9QDD5J

## Movements

| Movement          | Description                               | Time	|
|---                |---                                        |---	|
| Static            | Stand stil                                | ~10	|
| Walk              | Walk straight and back                    | ~30   | 
| Figure of 8       | Walk in figures of eight                  | ~60 	|
| Zig-Zag           | Walk zigzag                               | ~60  	|
| 5-minute walk     | Undirected walk, side step, and stand     | ~300 	|
| Speedskater       | Speedskater on the spot                   | ~30  	|
| Jog               | Jog straight and return                   | ~30  	|
| Jumping jacks     | Jumping jacks on the spot                 | ~30	|
| High kneee        | High knee jog straight and return         | ~30	|

**Disclaimer**: Be very careful here! As seen in the table above, the length of each sample differs. Very serious normalization job must be made here as we don't want to overfit the NN with a particular movement. 

## Measurement

Each sensor takes samples with ***100Hz*** frecuency (100 samples per second). 

### 1 - IMU (X-sens):

Not analized for now.

### 2 - VICON: 

This data set makes use in its format from the class `class +mocapdb.@ViconBody.ViconBody(varargin)`
* #### Data set structure

        Data set
        │
        └───Subject-01
        │   │
        │   └───Movement X1
        │   │       │   First Attempt
        │   │       │   Second Attempt
        │   │
        │   └───Movement X2
        │   │       │   First Attempt
        │   │       │   Second Attempt
        │   │ 
        │   ... (7 more movements)
        │   
        └───Subject-02
        │   │
        │   └───Movement X1
        │   
        ... (7 more subjects)
    

 + #### Position Variables (sensors): n x 3

    | Sensor    | Description   |
    |---        |---            |
    |  LTOE     | Right hip     | 
    |  PELV     | Left hip      |
    |  RFEP     | Right knee    |
    |  LFEP     | Left knee     |
    |  RFEO     | Right Ankle   | 
    |  LFEO     | Left Ankle    | 
    |  RTIO     | Right toe     | 
    |  LTIO     | Left toe      |

* #### Orientation Variables (sensors):  n x 4 

    | Sensor    | Description       |
    |---        |---                |
    |  qLSK     | Right foot        | 
    |  qRFT     | Left foot         |
    |  qLTH     | Right tibia       |
    |  qRSK     | Left tibia        |
    |  qRPV     | Right femur       | 
    |  qRTH     | Lef femur         | 
    
    **Unrecognized fields**: qLFT, RTOE (meassured and used -.-)
