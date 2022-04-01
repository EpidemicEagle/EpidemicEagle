import json 

f = open('disease_list.json')

js = json.load(f)
l = []
for i in js:
    print(i['name'])
    l.append(i['name'])

print(l)