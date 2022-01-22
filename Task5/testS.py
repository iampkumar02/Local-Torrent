import json
import pprint
json_data = None
with open('temp_file.json', 'r+') as f:
    data = f.read()
    json_data = json.loads(data)
prettyjson = pprint.pprint(json_data)
