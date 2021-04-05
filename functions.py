import json


def read_config(input_file):
    f = (open(input_file, "r+")).read()
    return json.loads(f)
