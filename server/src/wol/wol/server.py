#!/usr/bin/env python
import json
from pymongo import MongoClient
import db
from server_exceptions import PermissionDeniedException, WebException
from server_infrastructure import *
from wol import app

__author__ = 'archeg'

from flask import request,  jsonify
from db import DbService
import requests

db = DbService(MongoClient()["WOL"])

# TODO: Make it REST

@app.route("/")
def hello_world():
    return 'Hello World'


web_path = "/wol/api/v1.0/"


@app.route(web_path + "auth", methods=['POST'])
def auth():
    login, pwd, device_id = check_json_for_keys(["login", "pwd", "device_id"])
    token = db.authenticate(login, pwd, device_id)
    if not token:
        raise PermissionDeniedException()
    return jsonify({"token": token})


@app.route(web_path + "set_regid", methods=['POST'])
def renew_regid():

    checkAuth()
    login, device_id, reg_id = check_json_for_keys(["login", "device_id", "reg_id"])

    db.update_regid(login, device_id, reg_id)

    return jsonify()


@app.route(web_path + "get_devices", methods=['POST'])
def get_devices():

    checkAuth()
    login = check_json_for_keys(["login"])

    devices = db.get_deviceids(login)

    return jsonify({"devices": devices})


@app.route(web_path + "wake_device", methods=['POST'])
def send_wakeup():

    checkAuth()
    login, target_device = check_json_for_keys(["login", "target_device"])
    regId = db.get_regid(login, target_device)

    answer = requests.post("https://android.googleapis.com/gcm/send", data=json.dumps({"registration_ids": [regId]}), headers=get_google_header())

    google_response = json.loads(answer.content)
    if answer.status_code == 200:
        if google_response["failure"] == 0 and google_response["canonical_ids"] == 0:
            return "OK"

        # Error happened.
        return answer.content

    return "Received answer: " + answer.content, answer.status_code


@app.errorhandler(WebException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def checkAuth():
    login, device_id, token = check_json_for_keys(["login", "device_id", "token"])

    if not db.check_token(login, device_id, token):
        raise PermissionDeniedException()
