import os,glob
import json


def build_json(input_directory):
    json_config = '['
    counter = 0
    
    for item in glob.glob(os.path.join(input_directory, '*.json')):
        with open(item, 'r') as file:
            contents = file.read()
            json_config += contents + ','
            counter += 1

    json_config = json_config[:-1]
    json_config = json_config + ']'
    json_config = json.loads(json_config)
    return json_config

tiles_config = build_json('./plugins/tiles')
print(tiles_config)

navbar_config = build_json('./plugins/navbar')
print(navbar_config)

