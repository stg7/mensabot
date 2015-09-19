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
from mensabot import Mensaparser, get_pretty_name

from bottle import Bottle
from bottle import auth_basic
from bottle import route
from bottle import run
from bottle import template
from bottle import request
from bottle import redirect
from bottle import response
from bottle import error
from bottle import static_file

config = None


@route('/api/mensa/:mensaname')
def get_food(mensaname):
    if mensaname not in config["mensas"]:
        return {"status" : "unknown error"}
    res = {"status": "ok"}
    mp = Mensaparser(config["mensas"][mensaname], mensaname)
    res["res"] = mp.get_today()
    return res


@route('/subscribe')
@route('/subscribe', method="POST")
def subscribe():
    if "email" in request.forms and valid_mail(request.forms.get("email")):
        print(request.forms.get("email"))


    email = request.forms.get("email", "")
    selection = []
    time = request.forms.get("time", "")

    return template("templates/subscribe.tpl", title="MensaBot+",
                mensas={get_pretty_name(x): x for x in config["mensas"]},
                email=email, selection=selection, time=time, msg="")


@route('/unsubscribe')
def unsubscribe():
    return template("templates/unsubscribe.tpl", title="MensaBot+")


@route('/about')
def about():
    return template("templates/about.tpl", title="MensaBot+")


@route('/mensa/:mensaname')
def mensa(mensaname):
    if mensaname not in config["mensas"]:
        return index()
    return template("templates/mensa.tpl", title="MensaBot+ -- " + get_pretty_name(mensaname), mensa=get_pretty_name(mensaname), mensaname=mensaname, food=get_food(mensaname))


@route('/')
def index():
    return template("templates/index.tpl", title="MensaBot+", mensas={get_pretty_name(x): x for x in config["mensas"]})

@error(404)
def error404(error):
    return index()

@route("/favicon.ico")
def favicon():
    return server_static("favicon.ico")

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='templates/static')


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


    lInfo("server starting.")
    run(host='0.0.0.0', port=4223, debug=True, reloader=True)
    lInfo("server stopped.")


if __name__ == "__main__":
    main(sys.argv[1:])
