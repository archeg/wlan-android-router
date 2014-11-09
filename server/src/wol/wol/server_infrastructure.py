from flask import request
from configuration import ConfigService
from server_exceptions import InvalidFormatException

__author__ = 'archeg'

config = ConfigService()


def get_google_header():
    return {"Authorization": "key="+config.get_config("google-api-key"), "Content-Type": "application/json"}


def check_json_for_keys(keys):
    json = request.get_json()
    if not json:
        raise InvalidFormatException("Received empty data")
    if type(json) is not dict:
        raise InvalidFormatException("Data is not json-like dict")

    result = []
    for key in keys:
        if not json.has_key(key):
            raise InvalidFormatException("%s is not present" % key)
        else:
            result.append(json[key])

    if len(result) == 1:
        return result[0]

    return result


