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

# load libs from lib directory
import loader
from log import *
from system import *

config = None


def main(args):
    lInfo("start web interface for mensabot")
    lInfo("read config")
    # read config file
    try:
        global config
        config = json.loads(read_file(os.path.dirname(os.path.realpath(__file__)) + "/config.json"))
    except Exception as e:
        lError("configuration file 'config.json' is corupt (not json conform). error: " + str(e))
        return 1

    lInfo("...")
    jPrint(config)



if __name__ == "__main__":
    main(sys.argv[1:])
