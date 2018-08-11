#!/bin/bash

which celery
celery worker -A uservice_nbreport.celery.celery_app -E -l INFO
