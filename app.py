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
# Power options
#


@app.route('/power')
def power():
    return render_template('index.html',
                           config=config,
                           theme=theme,
                           utilities=utilities['utilities'],
                           page_name='power')


@app.route('/power/restart')
def shutdown():
    if os.name == 'nt':
        subprocess.call(config['utilities']
                        ['power_commands']['windows']['restart'])
    else:
        subprocess.call(config['utilities']
                        ['power_commands']['linux']['restart'])

    return render_template('return.html')


@app.route('/power/shutdown')
def shutdown():
    if os.name == 'nt':
        subprocess.call(config['utilities']
                        ['power_commands']['windows']['shutdown'])
    else:
        subprocess.call(config['utilities']
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
                # build the binary path as an exeplore application
                if 'windows_app' in tile:
                    bin_path = 'explorer.exe shell:appsFolder\\{}'.format(
                        tile['windows_app'])

                # If the windows_app key is not found, check for a
                # standard executable file, and start it
                elif 'executable' in tile:
                    bin_path = tile['executable']

        subprocess.call(bin_path)
        return render_template('return.html')

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
