from configuration import ConfigService
from server_exceptions import InvalidFormat

__author__ = 'archeg'

config = ConfigService()


def get_google_header():
    return {"Authorization": "key="+config.get_config("google-api-key"), "Content-Type": "application/json"}


def check_json_for_keys(keys, json):
    if not json:
        raise InvalidFormat("Received empty data")
    if type(json) is not dict:
        raise InvalidFormat("Data is not json-like dict")

    for key in keys:
        if not json.has_key(key):
            raise InvalidFormat("%s is not present" % key)

