# -*- coding:utf-8 -*-

import random

from pydecor import intercept

from util import on_exception, s, f


class Camt056Processor(object):

    def __init__(self):
        pass

    @intercept(catch=Exception, handler=on_exception)
    def process_camt_056_from_net(self, camt_056_message):
        """ camt.056 is a refund request message from WalletsNet, random approve or reject """

        orgnl_instr_id = camt_056_message['Document']['FIToFIPmtCxlReq']['Undrlyg']['TxInf']['OrgnlInstrId']
        amt = camt_056_message['Document']['FIToFIPmtCxlReq']['Undrlyg']['TxInf']['OrgnlIntrBkSttlmAmt']['Amount']
        ccy = camt_056_message['Document']['FIToFIPmtCxlReq']['Undrlyg']['TxInf']['OrgnlIntrBkSttlmAmt']['Ccy']

        decision = random.choice(['approve', 'reject'])

        if decision == 'approve':
            output = 'Approve refund request, amount={0} {1}, original instruction id={2}'. \
                format(amt, ccy, orgnl_instr_id)
            print(s(output))

            # Ack pacs.004 to trigger refund
        else:
            output = 'Reject refund request, amount={0} {1}, original instruction id={2}'. \
                format(amt, ccy, orgnl_instr_id)
            print(s(output))

            # Ack admi.029 to reject refund
