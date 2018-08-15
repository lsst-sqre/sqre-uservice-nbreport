##########
Change log
##########

0.2.0 (2018-08-15)
==================

This release is the first minimum viable product that accepts a notebook and converts it into an HTML report.

- New ``LsstHtmlReportExporter`` subclass of ``nbconvert``\ ’s ``HTMLConverter``.
  This subclass provides some defaults for the HTML converter, and also maintains knowledge of additional assets needed by the build.

- New ``LsstOutlinePreprocessor`` subclass of ``nbconvert``\ ’s ``Preprocessor``.
  This preprocessor analyzes the markdown header structure and creates a tree structure that is added to the resources dictionary under the ``lsst_outline`` key.
  The Jinja HTML templates use this tree to generate a hierarchical table of contents in the sidebar.

- New HTML and CSS theming for the notebooks.
  The CSS is generated with a Gulp pipeline from Sass.

- The ``POST /reports/<report>/instances/<instance_id>/notebook`` endpoint triggers a Celery queue task that actually transforms the notebook into HTML and uploads that HTML to LSST the Docs.

- New ``GET /queue/<id>`` endpoint for obtaining the status of a processing item in the queue.

0.1.1 (2018-08-09)
==================

- Set up the Kubernetes deployment, including templates for ConfigMaps and Secrets.

- Updated ``uwsgi.ini`` configuration that's compatible with the https://github.com/lsst-sqre/k8s-api-nginx frontend for api.lsst.codes.

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
