[![Build Status](https://travis-ci.org/lsst-sqre/uservice-nbreport.svg?branch=master)](https://travis-ci.org/lsst-sqre/uservice-nbreport)

# sqre-uservice-nbreport

LSST DM SQuaRE api.lsst.codes-compliant microservice wrapper.  TODO

## Usage

`sqre-uservice-nbreport` will run standalone on port
5000 or under `uwsgi`.  It responds to the following routes:

### Routes

* `/`: returns `OK` (used by Google Container Engine Ingress healthcheck)

* `/nbreport`: TODO

### Returned Structure

The returned structure is JSON.  TODO.
