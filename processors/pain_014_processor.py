# -*- coding:utf-8 -*-

import random

from pydecor import intercept

from util import on_exception, w, f


class Pain014Processor(object):

    def __init__(self):
        pass

    @intercept(catch=Exception, handler=on_exception)
    def process_pain_014_from_net(self, pain_014_message):
        """ pain_014_message is a rejection message from WalletsNet """

        print(w('Receive pain.014 message :('))
