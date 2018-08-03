.PHONY: help install run image travis-docker-deploy version basic

VERSION=$(shell FLASK_APP=uservice_nbreport flask version)

help:
	@echo "Make command reference"
	@echo "  make install ... (install app for development)"
	@echo "  make test ...... (run unit tests pytest)"
	@echo "  make run ....... (run Flask dev server)"
	@echo "  make image ..... (make tagged Docker image)"
	@echo "  make travis-docker-deploy (push image to Docker Hub from Travis CI)"
	@echo "  make version ... (print the app version)"
	@echo "  make basic ..... (convert basic.ipynb to html)"

install:
	pip install -e ".[dev]"

test:
	pytest --flake8 --cov=uservice_nbreport

run:
	FLASK_APP=uservice_nbreport FLASK_DEBUG=1 flask run

image:
	python setup.py sdist
	docker build --build-arg VERSION=$(VERSION) -t lsstsqre/uservice-nbreport:build .

travis-docker-deploy:
	./bin/travis-docker-deploy.bash lsstsqre/uservice-nbreport build

version:
	FLASK_APP=uservice_nbreport FLASK_DEBUG=1 flask version

basic:
	cd tests/notebooks && jupyter nbconvert --to uservice_nbreport.publish.htmlexport.LsstHtmlReportExporter basic.ipynb && cd ../..
