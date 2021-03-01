# LINUX Makefile

define help
Usage: make <command>
Commands:
  help:                 Show this help information
  develenv-up:			Launch the development environment with a docker-compose of the service
  preprocessing-sh:		Access to a shell of a launched preprocessing environment
  develenv-down:		Stop the development environment
endef
export help

help:
	@echo "$$help"

develenv-up:	
	@echo "Launching development environments"
	docker-compose build
	docker-compose up -d

develenv-down:
	@echo "Shutting down development environments"
	docker-compose down --remove-orphans

preprocess-sh:
	@echo "Entering preprocessing environment"
	docker exec -it "tfg_preprocesser_1" bash

process-sh:
	@echo "Entering processing environment"
	docker exec -it "tfg_processer_1" bash
