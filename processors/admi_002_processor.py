# -*- coding:utf-8 -*-

import random

from pydecor import intercept

from util import on_exception, w, f


class Admi002Processor(object):

    def __init__(self):
        pass

    @intercept(catch=Exception, handler=on_exception)
    def process_admi_002_from_net(self, admi_002_message):
        """ admi.002 is a rejection message from WalletsNet """

        print(w('Receive admi.002 message :('))
