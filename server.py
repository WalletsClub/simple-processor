# -*- coding:utf-8 -*-

import json

from flask import Flask, request, jsonify

from config import MY_SERVER_HOST, MY_SERVER_PORT
from util import j, pointer, highlight
from processors.pacs_008_processor import Pacs008Processor
from processors.pacs_009_processor import Pacs009Processor
from processors.pacs_002_processor import Pacs002Processor
from processors.pacs_004_processor import Pacs004Processor
from processors.camt_017_processor import Camt017Processor
from processors.camt_029_processor import Camt029Processor
from processors.pain_014_processor import Pain014Processor

app = Flask('my_server')


def process_it(message):
    """ process received message """

    scheme = message['AppHdr']['MsgDefIdr'][:8]

    if scheme == 'pacs.008':
        processor = Pacs008Processor()
        processor.process_pacs_008_from_net(message)
    elif scheme == 'pacs.009':
        processor = Pacs009Processor()
        processor.process_pacs_009_from_net(message)
    elif scheme == 'pacs.002':
        processor = Pacs002Processor()
        processor.process_pacs_002_from_net(message)
    elif scheme == 'pacs.004':
        processor = Pacs004Processor()
        processor.process_pacs_004_from_net(message)
    elif scheme == 'camt.017':
        processor = Camt017Processor()
        processor.process_camt_017_from_net(message)
    elif scheme == 'camt.029':
        processor = Camt029Processor()
        processor.process_camt_029_from_net(message)
    elif scheme == 'pain.014':
        processor = Pain014Processor()
        processor.process_pain_014_from_net(message)
    else:
        print('Can not process this message: {0}'.format(scheme))


@app.route('/', methods=['POST'])
def index():
    """ Process ISO messages forwarded from CLI """
    try:
        request_body = request.get_data()

        received_message = json.loads(request_body)
        scheme = received_message['AppHdr']['MsgDefIdr'][:8]

        print(pointer('My server receive message: ') + highlight('({0})'.format(scheme)))
        print(j(received_message))

        print(pointer('Processing...'))

        print(highlight('-' * 100))
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
