from flask import Flask, jsonify, render_template
import json
import os,glob
import time

app = Flask(__name__)

# Get time
sys_time = jsonify

# Build tiles configuration dictionary
tiles_config = '['
tiles_count = 0

tiles_dir = './plugins/tiles'
for tile in glob.glob(os.path.join(tiles_dir, '*.json')):
    with open(tile, 'r') as file:
        contents = file.read()
        tiles_config += contents + ','
        tiles_count += 1

tiles_config = tiles_config[:-1]
tiles_config = tiles_config + ']'
tiles_config = json.loads(tiles_config)

# Build navbar configuration dictionary
navbar_config = '['
navbar_count = 0

navbar_dir = './plugins/navbar'
for nav in glob.glob(os.path.join(navbar_dir, '*.json')):
    with open(nav, 'r') as file:
        contents = file.read()
        navbar_config += contents + ','
        navbar_count += 1

navbar_config = navbar_config[:-1]
navbar_config = navbar_config+ ']'
navbar_config = json.loads(navbar_config)

@app.route("/")
def home():
    return render_template('index.html', tiles_config=tiles_config, tiles_count=tiles_count, navbar_config=navbar_config)
