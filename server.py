# -*- coding:utf-8 -*-

import json

from flask import Flask, request, jsonify

from config import MY_SERVER_HOST, MY_SERVER_PORT
from util import j, pointer, highlight
from processors.pacs_008_processor import Pacs008Processor
from processors.pacs_002_processor import Pacs002Processor

app = Flask('my_server')


def process_it(message):
    """ process received message """

    scheme = message['AppHdr']['MsgDefIdr'][:8]

    if scheme == 'pacs.008':
        processor = Pacs008Processor()
        processor.process_pacs_008_from_net(message)
    elif scheme == 'pacs.002':
        processor = Pacs002Processor()
        processor.process_pacs_002_from_net(message)
    else:
        print('Can not process this message: {0}'.format(scheme))


@app.route('/', methods=['POST'])
def index():
    """ Process ISO messages forwarded from CLI """
    try:
        request_body = request.get_data()

        received_message = json.loads(request_body)

        print(pointer('My server receive message:'))
        print(j(received_message))

        print(pointer('Processing...'))

        print(highlight('-'*100))
        process_it(received_message)
        print(highlight('-' * 100))

        print(pointer('Done'))

        return jsonify(resultCode="T")
    except Exception as e:
        import traceback
        print('Error...')
        print(traceback.format_exc())
        return jsonify(resultCode="F")


if __name__ == "__main__":
    app.run(host=MY_SERVER_HOST, port=MY_SERVER_PORT, use_reloader=True, debug=True, ssl_context='adhoc')
