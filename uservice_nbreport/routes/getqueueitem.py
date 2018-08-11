__all__ = ('get_queue_item',)

from flask import jsonify, abort, url_for
from ..celery import celery_app

from . import api


@api.route('/queue/<id>', methods=['GET'])
def get_queue_item(id):
    try:
        task = celery_app.AsyncResult(id)
    except Exception:
        abort(404)

    data = {
        'id': id,
        'self_url': url_for('api.get_queue_item', id=id, _external=True),
        'status': task.state,
    }

    return jsonify(data), 200, {'Location': data['self_url']}
