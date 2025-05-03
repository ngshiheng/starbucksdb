NAME := starbucksdb
ENVIRONMENT ?= development

SHELL=/bin/bash
DATASETTE := $(shell command -v datasette 2> /dev/null)
DOCKER := $(shell command -v docker 2> /dev/null)
SQLITE_FILE = data/starbucks.db


.DEFAULT_GOAL := help
##@ Helper
.PHONY: help
help:	## display this help message.
	@echo "Welcome to $(NAME) [$(ENVIRONMENT)]."
	@awk 'BEGIN {FS = ":.*##"; printf "Use make \033[36m<target>\033[0m where \033[36m<target>\033[0m is one of:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


##@ Usage
.PHONY: run
run:	## run scraper.
	@rm -rf data/starbucks.db
	@uv run scrapy crawl singapore
	@echo "Done."

.PHONY: inspect
inspect:	## generate inspect file for performance optimization.
	@[ -f $(SQLITE_FILE) ] && echo "File $(SQLITE_FILE) exists." || { echo "File $(SQLITE_FILE) does not exist." >&2; exit 1; }
	@$(DATASETTE) inspect $(SQLITE_FILE) --inspect-file=data/inspect.json
	@echo "Generated inspect file at data/inspect.json"

.PHONY: datasette
datasette:	## run datasette with optimizations matching the Docker build.
	@[ -f $(SQLITE_FILE) ] && echo "File $(SQLITE_FILE) exists." || { echo "File $(SQLITE_FILE) does not exist." >&2; exit 1; }
	@if [ ! -f data/inspect.json ]; then $(MAKE) inspect; fi
	@$(DATASETTE) --immutable $(SQLITE_FILE) --inspect-file=data/inspect.json --setting allow_download off --setting allow_csv_stream off --setting max_csv_mb 1 --setting default_cache_ttl 604800 --metadata data/metadata.json


##@ Docker
IMAGE_NAME := ngshiheng/starbucksdb
TAG_DATE := $(shell date -u +%Y%m%d)

.PHONY: docker-build
docker-build:	## build datasette docker image.
	@[ -f $(SQLITE_FILE) ] && echo "File $(SQLITE_FILE) exists." || { echo "File $(SQLITE_FILE) does not exist." >&2; exit 1; }
	@if [ -z $(DATASETTE) ]; then echo "Datasette could not be found. See https://docs.datasette.io/en/stable/installation.html"; exit 2; fi
	datasette package $(SQLITE_FILE) --extra-options '--setting allow_download off --setting allow_csv_stream off --setting max_csv_mb 1 --setting default_cache_ttl 604800' --metadata data/metadata.json --install=datasette-cluster-map --install=datasette-gzip --install=datasette-block-robots --install=datasette-vega --install=datasette-google-analytics --tag $(IMAGE_NAME):$(TAG_DATE)
	datasette package $(SQLITE_FILE) --extra-options '--setting allow_download off --setting allow_csv_stream off --setting max_csv_mb 1 --setting default_cache_ttl 604800' --metadata data/metadata.json --install=datasette-cluster-map --install=datasette-gzip --install=datasette-block-robots --install=datasette-vega --install=datasette-google-analytics --tag $(IMAGE_NAME):latest

.PHONY: docker-push
docker-push:	## build and push docker images to registry.
	@if [ -z $(DOCKER) ]; then echo "Docker could not be found. See https://docs.docker.com/get-docker/"; exit 2; fi
	docker push $(IMAGE_NAME):$(TAG_DATE)
	docker push $(IMAGE_NAME):latest

##@ Contributing
.PHONY: clean
clean:	## clean all local cache.
	@find . -type d -name "__pycache__" | xargs rm -rf {};
	@rm -rf .scrapy

.PHONY: setup-dev
setup-dev:	## install development dependencies including required Datasette plugins.
	@if [ -z $(DATASETTE) ]; then echo "Installing Datasette..."; pip install datasette; fi
	@echo "Installing required Datasette plugins..."
	@pip install datasette-cluster-map datasette-gzip datasette-block-robots datasette-vega datasette-google-analytics
	@mkdir -p plugins
	@echo "Setup complete! Run 'make datasette' to start local development server."
