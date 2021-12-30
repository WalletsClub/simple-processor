# -*- coding:utf-8 -*-

from pydecor import intercept

from util import on_exception, s, f


class Pacs004Processor(object):

    def __init__(self):
        pass

    @intercept(catch=Exception, handler=on_exception)
    def process_pacs_004_from_net(self, pacs_004_message):
        """ pacs.004 is a refund message(copy) from WalletsNet, just credit user's account """

        orgnl_instr_id = pacs_004_message['Document']['PmtRtr']['TxInf']['OrgnlInstrId']
        amt = pacs_004_message['Document']['PmtRtr']['TxInf']['RtrdIntrBkSttlmAmt']['Amount']
        ccy = pacs_004_message['Document']['PmtRtr']['TxInf']['RtrdIntrBkSttlmAmt']['Ccy']

        output = 'Refund process succeeded, amount={0} {1}, original instruction id={2}'. \
            format(amt, ccy, orgnl_instr_id)
        print(s(output))
