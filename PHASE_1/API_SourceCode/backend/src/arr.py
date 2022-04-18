import json 

f = open('names.json')
data = json.load(f)


new_json = {}
for i in data:
    new_json[data[i]] = i


with open('country_codes.json', 'w') as g:
    g.write(json.dumps(new_json))
