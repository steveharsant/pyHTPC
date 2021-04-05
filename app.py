# Set linting rules
# pylint: disable=import-error
# pylint: disable=undefined-variable

from flask import Flask, jsonify, redirect, render_template, request
from pywinauto import Application

import errno
import json
import os
import subprocess

app = Flask(__name__)

#
# Initialisation
#

# Process config files


def read_config(input_file):
    f = (open(input_file, "r+")).read()
    return json.loads(f)


def reload_config():
    config_files = 'config.json', 'tiles.json', 'utilities.json'
    for conf in config_files:
        read_config('./{}'.format(conf))


# Read config to variables
config = read_config('./config.json')
tiles = read_config('./tiles.json')
utilities = read_config('./utilities.json')


# Load theme last as it relies on config to be loaded as well
theme = read_config(
    './static/themes/{}/theme.json'.format(config['theme']['active_theme']))

# Create temporary path if
# it does not already exist
if os.name == 'nt':
    temp_directory = "{}/thea".format(os.getenv('TEMP'))
else:
    temp_directory = '/tmp/thea'

try:
    os.makedirs(temp_directory)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

#
# Import plugins
#

plugins = [f for f in os.listdir('./plugins')]
for plugin in plugins:
    if plugin.endswith('.py'):
        exec(open('plugins/{}'.format(plugin)).read())

#
# Render Pages
#

exec(open('./routes.py').read())

#
# Start application
#

if __name__ == "__main__":
    app.run()
