# Set linting rules
# pylint: disable=import-error
# pylint: disable=undefined-variable

from flask import Flask, jsonify, redirect, render_template, request
from functions import read_config
from pywinauto import Application

import json
import errno
import os
import subprocess


app = Flask(__name__)

#
# Initialisation
#

# Dynamically read config to variables
config_files = [f for f in os.listdir('.')]
for c in config_files:
    if c.endswith('.json'):
        f = (open(c, "r+")).read()
        v = c.split('.')[0]
        globals()[v] = json.loads(f)
        print('loaded variable name: {}'.format(v))

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
