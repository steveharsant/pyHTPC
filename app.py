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
system_config = build_json('./')

@app.route('/')
def home():
    return render_template('index.html', tiles_config=tiles_config, navbar_config=navbar_config, system_config=system_config)

# Execute application
@app.route('/usr/bin/<app>')
def application(app):
    os.system('/usr/bin/' + app)
    return redirect('/')

@app.route('/tile-editor')
def tile_editor():
    return render_template('tile-editor.html', tiles_config=tiles_config, navbar_config=navbar_config)
    
@app.route('/tile-editor', methods=['POST'])
def tile_editor_post():
    tile_name = request.form['tile_name']; tile_filename = tile_name + '.json'; tile_name = "\"name\": \"" + tile_name + "\",\n"
    tile_info = request.form['tile_info']; tile_info = "\"info\": \"" + tile_info + "\",\n" 
    tile_url = request.form['tile_url']; tile_url = "\"url\": \"" + tile_url + "\",\n" 
    tile_type = request.form['tile_type']; tile_type = "\"type\": \"" + tile_type + "\",\n" 
    tile_catagory = request.form['tile_catagory']; tile_catagory = "\"catagory\": \"" + tile_catagory + "\",\n" 
    tile_favourite = request.form['tile_favourite']; tile_favourite = "\"favourite\": \"" + tile_favourite + "\"\n" 
    
    file = open('./plugins/tiles/' + tile_filename, 'w')
    file.writelines(['{\n', tile_name, tile_type, tile_catagory, tile_url, tile_info, tile_favourite, '}\n' ])
    file.close

    tiles_config = build_json('./plugins/tiles')
    return tile_editor()

@app.route('/settings')
def settings():
    return render_template('settings.html', system_config=system_config, navbar_config=navbar_config)

@app.route('/settings', methods=['POST'])
def settings_post():
    show_category_headers = request.form['show_category_headers']; show_category_headers = "\"showCatagoryHeaders\": \"" + show_category_headers + "\",\n"
    show_tile_headers = request.form['show_tile_headers']; show_tile_headers = "\"showTileHeaders\": \"" + show_tile_headers + "\",\n"
    show_tile_info = request.form['show_tile_info']; show_tile_info = "\"showTileInfo\": \"" + show_tile_info + "\",\n"
    categorise_tiles = request.form['categorise_tiles']; categorise_tiles = "\"categoriseTiles\": \"" + categorise_tiles + "\",\n"

    file = open('./config.json', w)
    file.writelines(['{\n', show_category_headers, show_tile_headers, show_tile_info, categorise_tiles, '}\n' ])
    file.close

    system_config = build_json('./')
    return settings_post()
