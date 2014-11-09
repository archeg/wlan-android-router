#!/usr/bin/env python
import json
from pymongo import MongoClient
import db
from server_infrastructure import *
from wol import app

__author__ = 'archeg'

from flask import request,  jsonify
from db import DbService
import requests

db = DbService(MongoClient()["WOL"])


@app.route("/")
def hello_world():
    return 'Hello World'


@app.route("/wol/api/v1.0/auth", methods=['POST'])
def auth():
    request_json = request.get_json(force=True)

    check_json_for_keys(["login", "pwd", "device_id"], request_json)
    login = request_json["login"]
    pwd = request_json["pwd"]
    device_id = request_json["device_id"]
    token = db.authenticate(login, pwd, device_id)
    if not token:
        raise InvalidFormat()
    return jsonify({"token": token})


@app.route("/wol/api/v1.0/send-wakeup", methods=['POST'])
def send_wakeup():
    request_json = request.get_json()
    userids = request_json["user_ids"]

    answer = requests.post("https://android.googleapis.com/gcm/send", data=json.dumps({"registration_ids": userids}), headers=get_google_header())

    google_response = json.loads(answer.content)
    if answer.status_code == 200:
        if google_response["failure"] == 0 and google_response["canonical_ids"] == 0:
            return "OK"

        return answer.content

    return "Received answer: " + answer.content, answer.status_code


@app.errorhandler(InvalidFormat)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
