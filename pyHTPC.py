from flask import Flask, jsonify, render_template
import json
import os,glob
import time

app = Flask(__name__)

# Get time
sys_time = jsonify

tiles_config = '['
tiles_count = 0

# Build tiles configuration dictionary
tiles_dir = './plugins/tiles'
for tile in glob.glob(os.path.join(tiles_dir, '*.json')):
    with open(tile, 'r') as file:
        contents = file.read()
        tiles_config += contents + ','
        tiles_count += 1

tiles_config = tiles_config[:-1]
tiles_config = tiles_config + ']'
tiles_config = json.loads(tiles_config)      

@app.route("/")
def home():
    return render_template('index.html', tiles_config=tiles_config, tiles_count=tiles_count)
