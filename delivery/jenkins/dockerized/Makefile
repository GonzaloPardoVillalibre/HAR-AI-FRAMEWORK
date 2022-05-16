# LINUX Makefile
# Aggregated makefile for jenkins scripts (DO NOT USE IN LOCAL!!)
PROJECT_NAME := framework
DOCKER_COMPOSE = docker-compose -p $(PROJECT_NAME)

define help

Usage: make <command>

Commands:
  help:                                  Show this help information
  build-interleaved-dataframes           Build interleaved dataframes for Unity representation
  filter-data                            Execute data-filtering script
  augment-data                           Execute data augmentation script
  pre-fe                                 Execute pre-segmentation feature extraction
  post-fe                                Execute post-segmentation feature extraction
  segment                                Execute segmentation script
  populate-fd                            Execute populate-final-dataset script
  run-pipeline                           Execute pre-process pipeline
  train                                  Start training process

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
	docker exec $$($(DOCKER_COMPOSE) ps -q preprocess | head -1) python3 -B ./pipeline/data-filtering/dataFiltering.py

augment-data:
	docker exec $$($(DOCKER_COMPOSE) ps -q preprocess | head -1) python3 -B ./pipeline/data-augmentation/dataAugmentation.py

pre-fe:
	docker exec $$($(DOCKER_COMPOSE) ps -q preprocess | head -1) python3 -B ./pipeline/features-extraction/preFeaturesExtraction.py

post-fe:
	docker exec $$($(DOCKER_COMPOSE) ps -q preprocess | head -1) python3 -B ./pipeline/features-extraction/postFeaturesExtraction.py

segment:
	docker exec $$($(DOCKER_COMPOSE) ps -q preprocess | head -1) python3 -B ./pipeline/segmentation/segmentation.py

populate-fd:
	docker exec $$($(DOCKER_COMPOSE) ps -q preprocess | head -1) python3 -B ./pipeline/populate-final-dataset/populateFinalDataset.py

train:
	docker exec $$($(DOCKER_COMPOSE) ps -q train | head -1) python3 -B ./main.py

run-pipeline: filter-data augment-data pre-fe segment post-fe populate-fd

