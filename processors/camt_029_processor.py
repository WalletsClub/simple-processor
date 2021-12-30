# -*- coding:utf-8 -*-

import random

from pydecor import intercept

from util import on_exception, w, f


class Camt029Processor(object):

    def __init__(self):
        pass

    @intercept(catch=Exception, handler=on_exception)
    def process_camt_029_from_net(self, camt_029_message):
        """ camt.029 is a rejection message from WalletsNet """

        print(w('Receive camt.029 message :('))
