from flask import Flask, jsonify, redirect, render_template, request
import json
import os
import subprocess

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


#
# Home screen
#


@app.route('/')
def home():
    return render_template('index.html',
                           tiles=tiles['tiles'],
                           config=config,
                           theme=theme,
                           utilities=utilities['utilities'],
                           page_name='home')

#
# Power options page
#


@app.route('/power')
def power():
    user_agent_string = request.headers.get('User-Agent')
    if 'Windows' in user_agent_string:
        client_os = 'windows'
    elif 'Linux' in user_agent_string:
        client_os = 'linux'
    elif 'Macintosh' in user_agent_string:
        client_os = 'mac'
    print('Client hit with user agent string: ' + user_agent_string)
    return render_template('index.html',
                           config=config,
                           client_os=client_os,
                           theme=theme,
                           utilities=utilities['utilities'],
                           page_name='power')

#
# Execute application
#


if os.name == 'nt':
    # Windows
    @app.route('/bin/<app>')
    def application(app):
        for tile in tiles['tiles']:
            if tile['name'] == app:
                bin_path = tile['path']
                break

        subprocess.call(bin_path)
        return redirect('/')
else:
    # Linux / MacOS
    @app.route('/usr/bin/<app>')
    def application(app):
        os.system('/usr/bin/' + app)
        return redirect('/')

#
# Start application
#

if __name__ == "__main__":
    app.run()
