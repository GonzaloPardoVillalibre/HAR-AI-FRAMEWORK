# LINUX Makefile
PROJECT_NAME := framework

define help

Usage: make <command>

Commands:
  help:                 Show this help information
  develenv-up:          Launch the development environment with a docker-compose of the service
  preprocess-sh:        Access to a shell of a launched preprocessing environment
  train-sh:             Access to a shell of a launched training environment
  inference-sh:         Access to a shell of a launched inference environment
  develenv-down:        Stop the development environment

endef
export help

help:
	@echo "$$help"

develenv-up:	
	@echo "Launching development environments"
	docker-compose build 
	docker-compose -p $(PROJECT_NAME) up -d

develenv-down:
	@echo "Shutting down development environments"
	docker-compose -p $(PROJECT_NAME) down --remove-orphans

preprocess-sh:
	@echo "Entering preprocessing environment"
	docker exec -it "$(PROJECT_NAME)_preprocesser_1" bash

train-sh:
	@echo "Entering train environment"
	docker exec -it "$(PROJECT_NAME)_trainer_1" bash

inference-sh:
	@echo "Entering inference environment"
	docker exec -it "$(PROJECT_NAME)_inferencer_1" bash
