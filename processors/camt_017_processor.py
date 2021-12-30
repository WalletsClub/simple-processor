# -*- coding:utf-8 -*-

import random

from pydecor import intercept

from util import on_exception, w, f


class Camt017Processor(object):

    def __init__(self):
        pass

    @intercept(catch=Exception, handler=on_exception)
    def process_camt_017_from_net(self, camt_017_message):
        """ camt.017 is a fx response message """

        print(w('Receive camt.017 message :)'))
