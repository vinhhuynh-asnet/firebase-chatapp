import sys

from flask import escape


def hello_http(request):
    """
    HTTP Cloud Function demo
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'

    return 'Hello {}!'.format(escape(name))

def hello_background(data, context):
    """
    Background Cloud Function demo
    """
    if data and 'name' in data:
        name = data['name']
    else:
        name = 'World'
    return 'Hello {}!'.format(name)

def hello_gcs(data, context):
    """
    Cloud Function triggered by GCS event
    """
    print("Sample file: {}.".format(data['objectId']))
    return True