import json 

f = open('reports.json')

js = json.load(f)['reports']

v = 0
r = 0
for i in js:
    i['reportId'] = r
    r += 1



a_file = open("reports_file.json", "w")
json.dump(js, a_file)
a_file.close()