[![Build Status](https://travis-ci.org/lsst-sqre/sqre-uservice-nbreport.svg?branch=master)](https://travis-ci.org/lsst-sqre/sqre-uservice-nbreport)

# sqre-uservice-nbreport

Service for LSST's notebook-based reports, hosted through api.lsst.codes. See [SQR-023: Design of the notebook-based report system](https://sqr-023.lsst.io) for background and https://nbreport.lsst.io for the client-side application.

## Endpoints

- `GET /`: returns `OK` (used by Google Container Engine Ingress healthcheck)

- `GET /nbreport/metadata`: service metadata.

- `POST /nbreports/`: register a new report.

- `POST /reports/<report>/instances/`: reserve a new report instance.

- `POST /reports/<report>/instances/<instance_id>/notebook`: upload a notebook file (`.ipynb`) for publication.
