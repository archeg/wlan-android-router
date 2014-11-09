from flask import Flask

__author__ = 'archeg'

app = Flask(__name__)

import wol.server
import wol.server_infrastructure