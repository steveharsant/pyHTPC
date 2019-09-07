from flask import Flask, jsonify, render_template, request
import json
import os,glob
import time

app = Flask(__name__)

# Get time
sys_time = jsonify

def build_json(input_directory):
        json_config = '['
        counter = 0
        
        for item in glob.glob(os.path.join(input_directory, '*.json')):
            with open(item, 'r') as file:
                contents = file.read()
                file.close()
                json_config += contents + ','
                counter += 1
    
        json_config = json_config[:-1]
        json_config = json_config + ']'
        json_config = json.loads(json_config)
        return json_config

# Build configurations
tiles_config = build_json('./plugins/tiles')
navbar_config = build_json('./plugins/navbar')


@app.route('/')
def home():
    return render_template('index.html', tiles_config=tiles_config, navbar_config=navbar_config)


@app.route('/settings', methods = ['GET', 'POST'])
def settings():
    if request.method == 'GET':
        return render_template('settings.html', tiles_config=tiles_config, navbar_config=navbar_config)
    else:
        # tile_name = request.form['tile_name']
        # tile_info = request.form['tile_info']
        # tile_url = request.form['tile_url']
        print('hello')
        home()