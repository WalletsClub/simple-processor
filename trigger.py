# -*- coding:utf-8 -*-

import json
import time

import requests

from messages.camt_056_msg import bake as bake_camt_056_msg
from messages.pacs_008_msg import bake as bake_pacs_008_msg
from messages.pacs_009_msg import bake as bake_pacs_009_msg
from messages.pain_013_msg import bake_rtp, bake_rff
from messages.pacs_028_msg import bake as bake_pacs_028_msg
from messages.camt_016_msg import bake as bake_camt_016_msg
from util import i, j, deep_set, highlight
from config import my_pid, net_pid, cp_pid, cli_server_address


def gen_camt_056_from_pacs_008(pacs_008_message):
    """ get camt.056 message from pacs.008 """
    camt_056_message = bake_camt_056_msg(my_pid, net_pid, cp_pid)

    deep_set(camt_056_message, 'Document.FIToFIPmtCxlReq.Undrlyg.OrgnlGrpInfAndCxl.OrgnlMsgId',
             pacs_008_message['Document']['FIToFICstmrCdtTrf']['GrpHdr']['MsgId'])

    deep_set(camt_056_message, 'Document.FIToFIPmtCxlReq.Undrlyg.OrgnlGrpInfAndCxl.OrgnlMsgNmId',
             pacs_008_message['AppHdr']['MsgDefIdr'])

    deep_set(camt_056_message, 'Document.FIToFIPmtCxlReq.Undrlyg.TxInf.OrgnlInstrId',
             pacs_008_message['Document']['FIToFICstmrCdtTrf']['CdtTrfTxInf']['PmtId']['InstrId'])

    deep_set(camt_056_message, 'Document.FIToFIPmtCxlReq.Undrlyg.TxInf.OrgnlEndToEndId',
             pacs_008_message['Document']['FIToFICstmrCdtTrf']['CdtTrfTxInf']['PmtId']['EndToEndId'])

    deep_set(camt_056_message, 'Document.FIToFIPmtCxlReq.Undrlyg.TxInf.OrgnlTxId',
             pacs_008_message['Document']['FIToFICstmrCdtTrf']['CdtTrfTxInf']['PmtId']['TxId'])

    deep_set(camt_056_message, 'Document.FIToFIPmtCxlReq.Undrlyg.TxInf.OrgnlIntrBkSttlmAmt.Ccy',
             pacs_008_message['Document']['FIToFICstmrCdtTrf']['GrpHdr']['TtlIntrBkSttlmAmt']['Ccy'])

    deep_set(camt_056_message, 'Document.FIToFIPmtCxlReq.Undrlyg.TxInf.OrgnlIntrBkSttlmAmt.Amount',
             pacs_008_message['Document']['FIToFICstmrCdtTrf']['GrpHdr']['TtlIntrBkSttlmAmt']['Amount'])

    deep_set(camt_056_message, 'Document.FIToFIPmtCxlReq.Undrlyg.TxInf.OrgnlIntrBkSttlmDt',
             pacs_008_message['Document']['FIToFICstmrCdtTrf']['GrpHdr']['IntrBkSttlmDt'])

    deep_set(camt_056_message, 'Document.FIToFIPmtCxlReq.Undrlyg.TxInf.CxlRsnInf.Rsn.Cd', 'CUST')

    return camt_056_message


def trigger_customer_credit_transfer():
    """ Trigger credit transfer process """
    # credit transfer first
    pacs_008_message = bake_pacs_008_msg(my_pid, net_pid, cp_pid, 'USD')
    r1 = requests.post(cli_server_address, data=json.dumps(pacs_008_message), timeout=5, verify=False)
    print(j(pacs_008_message))

    print(i('pacs.008 message has been sent'))


def trigger_cancel_credit_transfer():
    """ Trigger refund request process """
    # credit transfer first
    pacs_008_message = bake_pacs_008_msg(my_pid, net_pid, cp_pid, 'USD')
    print(i('Send pacs.008 request'))
    print(j(pacs_008_message))
    r1 = requests.post(cli_server_address, data=json.dumps(pacs_008_message), timeout=5, verify=False)

    print(highlight('-' * 100))
    print(i('Request for refund 10s later...'))
    time.sleep(10)
    print(highlight('-' * 100))

    # refund request
    camt_056_message = gen_camt_056_from_pacs_008(pacs_008_message)
    print(j(camt_056_message))
    r2 = requests.post(cli_server_address, data=json.dumps(camt_056_message), timeout=5, verify=False)

    print(i('Done, please check pacs.004 message...'))


def trigger_fi_credit_transfer():
    """ Trigger inter-wallet payment process """
    # credit transfer first
    pacs_009_message = bake_pacs_009_msg(my_pid, net_pid, cp_pid, 'USD')
    r1 = requests.post(cli_server_address, data=json.dumps(pacs_009_message), timeout=5, verify=False)

    print(j(pacs_009_message))
    print(i('pacs.009 message has been sent'))


def trigger_rtp():
    """ Trigger request to pay process """
    pain_013_message = bake_rtp(my_pid, net_pid, cp_pid, 'USD')

    print(j(pain_013_message))
    r2 = requests.post(cli_server_address, data=json.dumps(pain_013_message), timeout=5, verify=False)

    print(i('Request to Pay message has been sent'))


def trigger_query_rtp():
    """ Trigger query RtP """

    # send pain.013 first
    pain_013_message = bake_rtp(my_pid, net_pid, cp_pid, 'USD', 15)

    print(j(pain_013_message))
    r1 = requests.post(cli_server_address, data=json.dumps(pain_013_message), timeout=5, verify=False)

    print(i('Request to Pay message has been sent'))

    print(highlight('-' * 100))
    print(i('Request for query 10s later...'))
    time.sleep(10)
    print(highlight('-' * 100))

    pacs_028_message = bake_pacs_028_msg(my_pid, net_pid, cp_pid)
    pacs_028_message['Document']['FIToFIPmtStsReq']['TxInf']['OrgnlGrpInf']['OrgnlMsgId'] = \
        pain_013_message['Document']['CdtrPmtActvtnReq']['GrpHdr']['MsgId']
    pacs_028_message['Document']['FIToFIPmtStsReq']['TxInf']['OrgnlGrpInf']['OrgnlMsgNmId'] = \
        pain_013_message['AppHdr']['MsgDefIdr']
    pacs_028_message['Document']['FIToFIPmtStsReq']['TxInf']['OrgnlGrpInf']['OrgnlCreDtTm'] = \
        pain_013_message['Document']['CdtrPmtActvtnReq']['GrpHdr']['CreDtTm']
    print(j(pacs_028_message))

    r2 = requests.post(cli_server_address, data=json.dumps(pacs_028_message), timeout=5, verify=False)

    print(i('pacs.028 message has been sent, please check response pain.014 message'))


def trigger_rff():
    """ Trigger request for fee process """
    pain_013_message = bake_rff(my_pid, net_pid, cp_pid, 'USD')

    print(j(pain_013_message))
    r2 = requests.post(cli_server_address, data=json.dumps(pain_013_message), timeout=5, verify=False)

    print(i('Request for Fee message has been sent'))


def trigger_query_fx():
    """ Trigger query fx """
    camt_016_message = bake_camt_016_msg(my_pid, net_pid, cp_pid, 'HKD', 'USD')
    print(j(camt_016_message))

    r2 = requests.post(cli_server_address, data=json.dumps(camt_016_message), timeout=5, verify=False)

    print(i('camt.016 message has been sent, please check response camt.017 message'))


if __name__ == '__main__':
    trigger_rff()
