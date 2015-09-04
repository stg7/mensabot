#!/usr/bin/env python3
"""
    Copyright 2015-today
    Project Mensabot

    Author: Steve Göring
"""
import sys
import os
import argparse
import shelve
import json
import urllib.request
import signal
import time
from datetime import *

# load libs from lib directory
import loader
from log import *
from system import *

from bs4 import BeautifulSoup

config = None

class Mensaparser(object):
    _url = ""
    _name = ""
    __cache = None

    def __init__(self, mensaurl, name):
        self._url = mensaurl
        self._name = name
        name = "_".join(name.split())

        self.__cache = shelve.open(os.path.dirname(os.path.realpath(__file__)) + "/_" + name + "_cache")
        pass

    def get(self):
        key = datetime.now().strftime("%x|%H:%M")

        if key not in self.__cache:
            handle = urllib.request.urlopen(self._url)
            soup = BeautifulSoup(handle.read())
            self.__cache[key] = soup.prettify()

        return self.__cache[key]


def handler(signum, frame):
    print('Here you go')
    sys.exit(0)


def main(args):
    lInfo("start mensabot")
    lInfo("read config")
    # read config file
    try:
        global config
        config = json.loads(read_file(os.path.dirname(os.path.realpath(__file__)) + "/config.json"))
    except Exception as e:
        lError("configuration file 'config.json' is corupt (not json conform). error: " + str(e))
        return 1

    lInfo("...")
    signal.signal(signal.SIGINT, handler)

    jPrint(config)

    for mensaname in config["mensas"]:
        lInfo("parse mensa : {}".format(mensaname))
        url = config["mensas"][mensaname]
        mp = Mensaparser(url, mensaname)

        mp.get()




if __name__ == "__main__":
    main(sys.argv[1:])
