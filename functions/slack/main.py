import json
from flask import jsonify

import json

import apiclient
from flask import jsonify

# Config
with open('key.json', 'r') as f:
    data = f.read()
config = json.loads(data)

kgsearch = apiclient.discovery.build('kgsearch', 'v1',
                                     developerKey=config['KG_API_KEY'])

# Verify web hook for slack token
def verify_web_hook(form):
    if not form or form.get('token') != config['SLACK_TOKEN']:
        raise ValueError('Invalid request/credentials.')

# Format msg before output
def format_slack_message(query, response):
    entity = None
    if response and response.get('itemListElement') is not None and \
       len(response['itemListElement']) > 0:
        entity = response['itemListElement'][0]['result']

    message = {
        'response_type': 'in_channel',
        'text': 'Query: {}'.format(query),
        'attachments': []
    }

    attachment = {}
    if entity:
        name = entity.get('name', '')
        description = entity.get('description', '')
        detailed_desc = entity.get('detailedDescription', {})
        url = detailed_desc.get('url')
        article = detailed_desc.get('articleBody')
        image_url = entity.get('image', {}).get('contentUrl')

        attachment['color'] = '#3367d6'
        if name and description:
            attachment['title'] = '{}: {}'.format(entity["name"],
                                                  entity["description"])
        elif name:
            attachment['title'] = name
        if url:
            attachment['title_link'] = url
        if article:
            attachment['text'] = article
        if image_url:
            attachment['image_url'] = image_url
    else:
        attachment['text'] = 'No results match your query.'
    message['attachments'].append(attachment)

    return message


def make_search_request(query):
    req = kgsearch.entities().search(query=query, limit=1)
    res = req.execute()
    return format_slack_message(query, res)

# Only accept POST request
def kg_search(request):
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405

    verify_web_hook(request.form)
    kg_search_response = make_search_request(request.form['text'])
    return jsonify(kg_search_response)
