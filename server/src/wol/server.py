#!/usr/bin/env python
import json
from pymongo import MongoClient
from configuration import ConfigService
import db

__author__ = 'archeg'

from flask import Flask
from flask import request
import requests

app = Flask(__name__)
config = ConfigService()
db = db.DbService(MongoClient()["WOL"])


@app.route("/")
def hello_world():
    return 'Hello World'


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


def get_google_header():
    return {"Authorization": "key="+config.get_config("google-api-key"), "Content-Type": "application/json"}

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
