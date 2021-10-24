# LINUX Makefile

define help

Usage: make <command>

Commands:
  help:                                  Show this help information
  build-interleaved-dataframes           Build interleaved dataframes for Unity representation
  filter-data                            Execute data-filtering script
  augment-data                           Execute data augmentation script
  segment                                Execute segmentation script
  run-pipeline                           Execute pre-processing pipeline 

Usual order:
  1. filter-data
  2. augment-data
  3. segment

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

segment:
	python3 -B ./pipeline/segmentation/segmentation.py

run-pipeline: filter-data augment-data segment
