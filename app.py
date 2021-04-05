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

# Render Homepage


@app.route('/')
def home():
    # config = read_config('./config.json')
    reload_config()
    return render_template('index.html',
                           tiles=tiles['tiles'],
                           config=config,
                           theme=theme,
                           utilities=utilities['utilities'],
                           page_name='home',
                           temp=temp)


# Render all other pages
@ app.route('/<page_name>')
def load_page(page_name):
    print('Loading {}'.format(page_name))
    return render_template('index.html',
                           config=config,
                           theme=theme,
                           utilities=utilities['utilities'],
                           page_name=page_name,
                           temp=temp)


#
# Power options
#

@ app.route('/power/restart')
def shutdown():
    if os.name == 'nt':
        os.system(config['utilities']
                        ['power_commands']['windows']['restart'])
    else:
        os.system(config['utilities']
                        ['power_commands']['linux']['restart'])

    return render_template('return.html')


@app.route('/power/shutdown')
def restart():
    if os.name == 'nt':
        os.system(config['utilities']
                        ['power_commands']['windows']['shutdown'])
    else:
        os.system(config['utilities']
                        ['power_commands']['linux']['shutdown'])

    return render_template('return.html')

#
# Execute application
#


if os.name == 'nt':

    # Windows
    @app.route('/app/<app>')
    def application(app):

        print('Launching application: {}'.format(app))
        for tile in tiles['tiles']:
            if tile['location'] == '/app/{}'.format(app):

                # If the Windows app key is found within the dictionary,
                # build the binary path as an explorer application
                if 'windows_app' in tile:
                    bin_path = 'explorer.exe shell:appsFolder\\{}'.format(
                        tile['windows_app'])

                # If the windows_app key is not found, check for a
                # standard executable file, and start it
                elif 'executable' in tile:
                    bin_path = tile['executable']

        # Start process and bring process to front
        process = subprocess.Popen(bin_path)

        try:
            app = Application().connect(process=process.pid)
            app.top_window().set_focus()
        except Exception as e:
            print(e)

        return render_template('return.html')

else:
    # Linux / MacOS
    @app.route('/usr/bin/<app>')
    def application(app):
        os.system('/usr/bin/' + app)
        return redirect('/')

#
# Open settings
#

if os.name == 'nt':

    # Windows
    @app.route('/settings/<settings>')
    def settings(settings):

        print('Launching settings option: {}'.format(settings))
        for setting in config['settings']:
            if setting['location'] == '/settings/{}'.format(settings):
                command = 'cmd /c start ms-settings:{}'.format(
                    setting['name']).lower()

        subprocess.Popen(command)
        return redirect('/')
else:
    # Linux / MacOS
    @app.route('/app/<settings>')
    def settings(settings):
        return render_template('apologies.html')

#
# Start application
#

if __name__ == "__main__":
    app.run()
