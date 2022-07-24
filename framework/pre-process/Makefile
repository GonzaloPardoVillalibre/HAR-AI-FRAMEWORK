# LINUX Makefile

define help

Usage: make <command>
Commands:
    help:                                  Show this help information
  
    #########################
   #  UNITY-REPRESENTATION #
  #########################
    build-interleaved-dataframes           Build interleaved dataframes for Unity representation
  
    #########################
   # PRE-PROCESS PIPELINE  #
  #########################
    filter-data                            Execute data-filtering script
    augment-data                           Execute data augmentation script
    pre-segmentation-fe                    Execute pre-segmentation feature extraction
    post-segmentation-fe                   Execute post-segmentation feature extraction
    segment                                Execute segmentation script
    populate-fd                            Execute populate-final-dataset script
    run-pipeline                           Execute pre-process pipeline 

    Usual order:
      1. filter-data
      2. augment-data
      3. pre-fe
      4. segment
      5. post-fe
      6. populate-fd

endef
export help

help:
	@echo "$$help"

build-interleaved-dataframes:
	python3 -B ./unity/interleaved-dataframe/main.py

filter-data:
	python3 -B ./pipeline/data-filtering/dataFiltering.py

augment-data:
	python3 -B ./pipeline/data-augmentation/dataAugmentation.py

pre-fe:
	python3 -B ./pipeline/features-extraction/preFeaturesExtraction.py

post-fe:
	python3 -B ./pipeline/features-extraction/postFeaturesExtraction.py

segment:
	python3 -B ./pipeline/segmentation/segmentation.py

populate-fd:
	python3 -B ./pipeline/populate-final-dataset/populateFinalDataset.py

run-pipeline: filter-data augment-data pre-fe segment post-fe populate-fd
