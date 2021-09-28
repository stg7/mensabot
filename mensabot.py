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
import ssl
import signal
from time import sleep
from datetime import *
import re

# load libs from lib directory
import loader
from log import *
from system import *

from bs4 import BeautifulSoup

# ignore ssl errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

DEBUG = True

config = None

API = """
"""

def get_date_str():
    return datetime.now().strftime("%Y-%m-%d")


def get_day_name():
    daynames = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    day = datetime.today().weekday()
    return daynames[day]


def get_pretty_name(x):
    return " ".join([y.title() for y in x.split("_")])


class Mensaparser(object):
    _url = ""
    _name = ""
    __cachename = ""

    def __init__(self, mensaurl, name):
        self._url = mensaurl
        self._name = name
        name = "_".join(name.split())
        self.__cachename = os.path.dirname(os.path.realpath(__file__)) + "/_" + name + "_cache"

    # def _parse_day(self, node):
    #     dishes = []
    #     for row in node.find_all("tr"):
    #         cols = row.find_all("td")
    #         if cols == []:
    #             continue
    #         where = cols[0].get_text().replace("Mittag", " ").strip()
    #         what = re.sub("\s+", " ", re.sub("\nInhalt:.*", "", cols[1].get_text()).strip())
    #         price = cols[2].get_text().strip()
    #         dishes +=[(where, what, price)]
    #     return dishes

    def get(self, debug=True):
        key = datetime.now().strftime("%x|%H")
        __cache = shelve.open(self.__cachename)

        if key not in __cache or debug:
            try:
                handle = urllib.request.urlopen(self._url, context=ctx)
            except Exception as e:
                print(e)
                print(self._url)
                return ""

            content = handle.read().decode("utf-8", "replace")
            soup = BeautifulSoup(content, "html.parser")
            dishes = []
            for meal in soup.find_all(class_="rowMealInner"):
                what = meal.find_all(class_="mealText")[0].get_text().strip()
                price = meal.find_all(class_="mealPreise")[0].get_text().strip()
                dishes.append([what, price])

            __cache[key] = [dishes]

        return __cache[key]

    def get_today(self):
        return self.get()[0]


class EmailNotifiyer(object):
    _from_pw = ""
    _from_username = ""

    def __init__(self, username, password):
        self._from_pw = password
        self._from_username = username

    def _send(self, user, user_msg):
        if user == "" or "@" not in user:
            lError("email not valid: {}".format(user))
            return
        if user_msg == {}:
            return

        lInfo("send to {} : ".format(user) + pPrint(list(user_msg.keys()), False))

        sendmsg = ""
        for key in  sorted(user_msg.keys()):
            if user_msg[key] == []:
                continue
            mensaname = get_pretty_name(key)
            sendmsg += mensaname + "<br>\n" + "-" * len(mensaname) + "<br>\n"
            for food in user_msg[key]:
                sendmsg += "{what}: {price} <br>\n".format(what=food[0], price=food[1])
            sendmsg += "<br>\n"

        if sendmsg == "":
            return

        sendmsg += API

        import smtplib
        from email.mime.text import MIMEText
        from email.header import Header

        msg = MIMEText(sendmsg, 'html', _charset="UTF-8")

        msg['From'] = self._from_username
        msg['To'] = user
        msg['Subject'] = Header('[MensaBot+] ' + get_day_name() + " " + get_date_str(), "utf-8")

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(self._from_username, self._from_pw)
        try:
            server.sendmail(self._from_username, user, msg.as_string())
        except:
            lError("Unexpected error while sending:"+ str(sys.exc_info()[0]))

        server.quit()


    def notify(self, users, mensas):
        lInfo("notify...")
        user_time = {}
        for user in users:
            time_slots = {}
            for x in users[user]:
                time_slots[x["send_time"]] = time_slots.get(x["send_time"], []) + [x["mensa"]]
            user_time[user] = time_slots

        hour = datetime.now().strftime("%H:")

        for user in user_time:
            matching_slots = [k for k in user_time[user] if hour in k]

            user_msg = {}
            for slot in matching_slots:
                for mensa in user_time[user][slot]:
                    user_msg[mensa] = mensas[mensa].get_today()
            self._send(user, user_msg)


def ctrl_c_handler(signum, frame):
    print('Here you go')
    sys.exit(0)


def load_users(userfile):
    return json.loads(read_file(os.path.dirname(os.path.realpath(__file__)) + "/" + userfile))


def main(args):
    lInfo("start mensabot")
    lInfo("read config")
    # todo: config file as cli-parameter/default value
    # read config file
    try:
        global config
        config = json.loads(read_file(os.path.dirname(os.path.realpath(__file__)) + "/config.json"))
    except Exception as e:
        lError("configuration file 'config.json' is corupt (not json conform). error: " + str(e))
        return 1

    signal.signal(signal.SIGINT, ctrl_c_handler)

    # create all mensaparsers
    mensas = {}
    for mensaname in sorted(config["mensas"].keys()):
        mensas[mensaname] = Mensaparser(config["mensas"][mensaname], mensaname)
        print(mensas[mensaname].get_today())

    userfile_path = os.path.dirname(os.path.realpath(__file__)) + "/" + config["users_file"]

    if not os.path.isfile(userfile_path):
        lWarn("usersfile is empty, create initial file")
        f = open(userfile_path, "w")
        f.write(jPrint({}, False))
        f.close()

    notifiers = []
    if config["email_sending"]:
        notifiers.append(EmailNotifiyer(config["email_user"], config["email_password"]))

    while True:
        # load userfile in each iteration, because some things can be changed
        users = load_users(config["users_file"])

        for notifier in notifiers:
            notifier.notify(users, mensas)

        sleep_time = 60 - datetime.now().minute
        lInfo("sleep " + str(sleep_time) + " mins")
        sleep((sleep_time) * 60)


if __name__ == "__main__":
    main(sys.argv[1:])
