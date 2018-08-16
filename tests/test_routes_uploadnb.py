"""Tests for POST /reports/<report>/instance/<id>/notebook
"""

import responses
import nbformat


@responses.activate
def test_upload_instance(client, github_auth_header, mocker):
    responses.add(
        responses.GET,
        'https://api.github.com/user',
        status=200,
        json={
            'login': 'testuser'
        }
    )
    responses.add(
        responses.GET,
        'https://api.github.com/user/orgs',
        status=200,
        json=[
            {
                'login': 'lsst'
            }
        ]
    )
    responses.add(
        responses.GET,
        'https://keeper.lsst.codes/token',
        status=200,
        json={'token': 'ltdtoken'}
    )

    mock_task = mocker.patch(
        'uservice_nbreport.routes.uploadnb.publish_instance')
    mock_url_for = mocker.patch(
        'uservice_nbreport.routes.uploadnb.url_for')
    mock_url_for.return_value = 'https://example.com/12345'

    # Create a mock notebook
    nb = nbformat.v4.new_notebook()
    nb.cells.append(
        nbformat.v4.new_markdown_cell(source='Hello world')
    )
    nb_data = nbformat.writes(nb, version=4)

    with client:
        headers = dict(github_auth_header)
        headers['Content-Type'] = 'application/x-ipynb+json'
        response = client.post(
            '/nbreport/reports/testr-000/instances/1/notebook',
            headers=headers,
            data=nb_data
        )
        assert response.status_code == 202

        mock_task.apply_async.assert_called_once()
        mock_url_for.assert_called_once()
