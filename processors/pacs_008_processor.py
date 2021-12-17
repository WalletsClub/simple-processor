# -*- coding:utf-8 -*-

import json

import requests
from pydecor import intercept

from messages.pacs_002_msg import bake
from util import on_exception, s, f
from config import my_pid, net_pid, cli_server_address


class Pacs008Processor(object):

    def __init__(self):
        pass

    @intercept(catch=Exception, handler=on_exception)
    def process_pacs_008_from_net(self, pacs_008_message):
        """ process pacs.008 message from WalletsNet, if:
            (1) You approve the transaction, feedback with positive pacs.002
            (2) You reject the transaction, feedback with negative pacs.002
        """
        pacs_002_message = bake(my_pid, net_pid)

        pacs_002_message['Document']['FIToFIPmtStsRpt']['OrgnlGrpInfAndSts']['OrgnlCreDtTm'] \
            = pacs_008_message['Document']['FIToFICstmrCdtTrf']['GrpHdr']['CreDtTm']

        pacs_002_message['Document']['FIToFIPmtStsRpt']['OrgnlGrpInfAndSts']['OrgnlMsgId'] \
            = pacs_008_message['AppHdr']['BizMsgIdr']

        pacs_002_message['Document']['FIToFIPmtStsRpt']['TxInfAndSts']['InstgAgt']['FinInstnId']['ClrSysMmbId']['MmbId'] \
            = pacs_008_message['Document']['FIToFICstmrCdtTrf']['CdtTrfTxInf']['InstdAgt']['FinInstnId']['ClrSysMmbId'][
            'MmbId']

        pacs_002_message['Document']['FIToFIPmtStsRpt']['TxInfAndSts']['InstdAgt']['FinInstnId']['ClrSysMmbId']['MmbId'] \
            = pacs_008_message['Document']['FIToFICstmrCdtTrf']['CdtTrfTxInf']['InstgAgt']['FinInstnId']['ClrSysMmbId'][
            'MmbId']

        pacs_002_message['Document']['FIToFIPmtStsRpt']['TxInfAndSts']['OrgnlInstrId'] \
            = pacs_008_message['Document']['FIToFICstmrCdtTrf']['CdtTrfTxInf']['PmtId']['TxId']

        # Approve the transaction
        pacs_002_message['Document']['FIToFIPmtStsRpt']['TxInfAndSts']['TxSts'] = 'RCVD'

        # feedback via cli tool
        response = requests.post(cli_server_address, data=json.dumps(pacs_002_message), timeout=5)

        if response.status_code == 200:
            print(s(' Feedback succeeded'))
        else:
            print(f(' Feedback failed'))
