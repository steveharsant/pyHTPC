from flask import Flask, jsonify, redirect, render_template, request
import json
import os

app = Flask(__name__)


def read_config(input_file):
    f = (open(input_file, "r+")).read()
    return json.loads(f)


# Read config to variables
config = read_config('./config.json')
tiles = read_config('./tiles.json')
utilities = read_config('./utilities.json')

# Load theme last as it relies on config to be loaded as well
theme = read_config(
    './static/themes/{}/theme.json'.format(config['theme']['active_theme']))

print(type(tiles))
print(type(utilities))

#
# Home screen
#


@app.route('/')
def home():
    return render_template('index.html', tiles=tiles['tiles'], config=config, theme=theme)

#
# Execute application
#


@app.route('/usr/bin/<app>')
def application(app):
    os.system('/usr/bin/' + app)
    return redirect('/')
