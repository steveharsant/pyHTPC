import os,glob
import json
import ast
# tiles_config = '''
# {
#     "tiles": [
# '''

# tiles_dir = '/home/steve/projects/pyHTPC/plugins/tiles'
# for tile in glob.glob(os.path.join(tiles_dir, '*.json')):
#     with open(tile, 'r') as file:
#         contents = file.read()
#         tiles_config = tiles_config + contents + ','
    
# tiles_config = tiles_config[:-1]
# tiles_config = tiles_config + ']}'
# tiles_config = json.loads(tiles_config)

# for title in tiles_config['tiles']:
#     print(title['title'])



#tiles_config = ast.literal_eval("{'muffin' : 'lolz', 'foo' : 'kitty'}")
tiles_config = '['
tiles_dir = '/home/steve/projects/pyHTPC/plugins/tiles'
for tile in glob.glob(os.path.join(tiles_dir, '*.json')):
    with open(tile, 'r') as file:
        contents = file.read()
        tiles_config += contents + ','

tiles_config = tiles_config[:-1]
tiles_config = tiles_config + ']'
tiles_config = json.loads(tiles_config)


# for title in tiles_config['tiles']:
#     print(title.name)
# print(tiles_config['name'][1])



print(type(tiles_config[0]))


# print(tiles_config[0]['name'])
# print(tiles_config)

# items = [{'text' : 'first'}, {'text' : 'second'}, {'text' : 'third'}]
# print(type(items[0]))