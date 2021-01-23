# LINUX Makefile

define help
Usage: make <command>
Commands:
  help:                         Show this help information
  vicon-pre-processing          Pre-process vicon dataset to feat NN input model.
  build-interleaved-dataframe   Excute interleaved dataframe script.
  build-image-builder           Excute image builder script.
  build-image-enricher          Excute image enricher script.
  build-final-dataset           Excute final dataset script.
endef
export help

help:
	@echo "$$help"

build-interleaved-dataframe:
	python3 ./interleaved-dataframe/scripts/processing.py

build-image-builder:
	python3 ./image-builder/scripts/processing.py

build-image-enricher:
	python3 ./image-enricher/scripts/processing.py

build-final-dataset:
	python3 ./final-dataset/scripts/processing.py

build-all: build-interleaved-dataframe build-image-builder build-image-enricher build-final-dataset