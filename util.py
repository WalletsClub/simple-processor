# -*- coding:utf-8 -*-

import json
from functools import reduce

from prettytable import PrettyTable
from tabulate import tabulate
from termcolor import colored


def on_exception(exc):
    """ Just print exception stdout """
    print(type(exc))
    print('Non-critical exception happened: {0}'.format(exc))


def deep_get(dictionary, key_chain, default=None):
    """ Get value from dict via key chain string """
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, key_chain.split("."),
                  dictionary)


def deep_set(dictionary, key_chain, value):
    """ Set value to dict via key chain string """
    keys = key_chain.split('.')
    for key in keys[:-1]:
        dictionary = dictionary.setdefault(key, {})
    dictionary[keys[-1]] = value


def table(d):
    """ Print dict as table view """
    try:
        x = PrettyTable()
        x.field_names = d.keys()
        x.add_row(d.values())
        return x
    except:
        return d


def j(d):
    """ Print dict as json view """
    try:
        d.pop('_id', None)

        return json.dumps(d, indent=4, default=str, ensure_ascii=False)
    except:
        return d


def s(text):
    """ return success text """
    try:
        return colored('[√] ', 'green') + text
    except:
        return text


def f(text):
    """ return fail text """
    try:
        return colored('[×] ', 'red') + text
    except:
        return text


def w(text):
    """ return warning text """
    try:
        return colored('[!] ', 'yellow') + text
    except:
        return text


def pointer(text):
    """ return pointer + text """
    try:
        return colored('-----> ', 'red') + text
    except:
        return text


def highlight(text):
    """ return red text """
    try:
        return colored(text, 'yellow')
    except:
        return text


def border(text):
    """ Print text with border """
    try:
        tb = [[text]]
        output = tabulate(tb, tablefmt='grid')
        return output
    except:
        return text
