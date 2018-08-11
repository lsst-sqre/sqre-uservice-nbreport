"""Tests for the `uservice_nbreport.tasks.publishnb` module.
"""

import responses

from uservice_nbreport.tasks.publishnb import get_edition_url


@responses.activate
def test_get_edition_url():
    responses.add(
        responses.GET,
        'https://keeper.lsst.codes/products/testr-000/editions/',
        status=200,
        json={
            'editions': [
                'https://keeper.lsst.codes/editions/119',
                'https://keeper.lsst.codes/editions/120'
            ]
        }
    )
    responses.add(
        responses.GET,
        'https://keeper.lsst.codes/editions/120',
        status=200,
        json={
            'slug': 'test',
        }
    )
    responses.add(
        responses.GET,
        'https://keeper.lsst.codes/editions/119',
        status=200,
        json={
            'slug': '1'
        }
    )

    edition_url = get_edition_url(
        keeper_url='https://keeper.lsst.codes',
        ltd_token='testtoken',
        ltd_product='testr-000',
        instance_id='1')

    assert edition_url == 'https://keeper.lsst.codes/editions/119'
