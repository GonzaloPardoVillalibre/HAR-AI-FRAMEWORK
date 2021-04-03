-----------------------------------------
# Framework 

## Data structure


       Framework
        │
        └─── final-dataset
        │   
        └─── inference 
        │   
        └─── pre-processing
        │   
        └─── train

* #### final-dataset
    Volume shared by both environments. In any case, the developer should store the training dataset here; either if it comes from the pre-processing environment or it is pre-processed externally.

* #### inference
    Contains all the data for the inference API.

* #### pre-processing
    Contains all the scripts for the preprocessing environment.

* #### train
    Contains all the scripts for the training environment.
