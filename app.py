from flask import Flask, jsonify, redirect, render_template, request
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

# # Execute application
# @app.route('/usr/bin/<app>')
# def application(app):
#     os.system('/usr/bin/' + app)
#     return redirect('/')

@app.route('/settings')
def settings():
    return render_template('settings.html', tiles_config=tiles_config, navbar_config=navbar_config)
    
@app.route('/settings', methods=['POST'])
def settings_post():
    tile_name = request.form['tile_name']; tile_filename = tile_name + '.json'; tile_name = "\"name\": \"" + tile_name + "\",\n"
    tile_info = request.form['tile_info']; tile_info = "\"info\": \"" + tile_info + "\",\n" 
    tile_url = request.form['tile_url']; tile_url = "\"url\": \"" + tile_url + "\",\n" 
    tile_type = request.form['tile_type']; tile_type = "\"type\": \"" + tile_type + "\",\n" 
    tile_catagory = request.form['tile_catagory']; tile_catagory = "\"catagory\": \"" + tile_catagory + "\",\n" 
    tile_favourite = request.form['tile_favourite']; tile_favourite = "\"favourite\": \"" + tile_favourite + "\"\n" 
    
    file = open('./plugins/tiles/' + tile_filename, 'w')
    file.writelines(['{\n', tile_name, tile_type, tile_catagory, tile_url, tile_info, tile_favourite, '}\n' ])
    file.close

    return settings()

# Execute application
@app.route('/usr/bin/<app>')
def application(app):
    os.system('/usr/bin/' + app)
    return redirect('/')