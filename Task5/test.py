import json

with open('temp_file.json', 'r') as f:
    json_data = json.load(f)
    user = json_data['users']
    l = (len(user))
    for i in range(0, l):
        name = user[i]['username']
        if name == "iampkumar":
            user[i]['count'] = 1000

with open('temp_file.json', 'w') as f:
    f.write(json.dumps(json_data))
