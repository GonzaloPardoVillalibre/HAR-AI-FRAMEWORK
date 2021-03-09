-----------------------------------------
# Framework 

## Data structure


       Framework
        │
        └─── final-dataset
        │   
        └─── pre-processing
        │   
        └─── train

* #### final-dataset
    Volume shared by both environments. In any case, the developer should store the training dataset; either if it comes from the pre-processing environment or it is pre-processed externally.

* #### pre-processing
    Contains all the scripts needed for the preprocessing environment. It includes also some test files.

* #### train
    Contains all the scripts for the training environment. It includes also some test files.
