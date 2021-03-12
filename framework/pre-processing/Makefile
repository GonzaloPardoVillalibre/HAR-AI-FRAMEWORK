# LINUX Makefile

define help

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

endef
export help

help:
	@echo "$$help"

build-interleaved-dataframes:
	python3 ./interleaved-dataframe/scripts/processing.py

build-images:
	python3 ./image-builder/scripts/processing.py

enrich-images:
	python3 ./image-enricher/scripts/processing.py

build-final-dataset:
	python3 ./final-dataset/scripts/processing.py

build-all: build-interleaved-dataframe build-image-builder build-image-enricher build-final-dataset
