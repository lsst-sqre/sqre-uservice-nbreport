##########
Change log
##########

0.1.0 (2018-08-08)
==================

First development release of ``uservice_nbreport``.

- Initialized repository from https://github.com/lsst-sqre/uservice-bootstrap and further customized the Flask application around an application factory and blueprints.

- Implemented GitHub personal access token-based authentication and GitHub organization-based authentication.

- Implemented a ``POST /nbreport/reports/`` endpoint to register new reports.
  On the backend, this command creates a new product on LSST the Docs.

- Implemented a ``POST /reports/<report>/instances/`` endpoint to reserve a new instance identifier.
  On the backend, this command creates a new edition on LSST the Docs.
  It uses LTD Keeper's new ``autoincrement`` feature.

- Stubbed out a ``POST /reports/<report>/instances/<instance_id>/notebook`` endpoint to upload notebooks (ipynb) to.
  Currently this endpoint doesn't do anything with the notebook.
