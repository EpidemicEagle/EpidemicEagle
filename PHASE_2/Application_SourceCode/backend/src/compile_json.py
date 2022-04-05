import json 

f = open('reports.json')

js = json.load(f)['reports']

v = 0
r = 0
for i in js:
    i['reportId'] = r
    
    # 1996-01-22T00:00:00.000Z
    i['eventDate'] = i['eventDate'][:10]
    r += 1




a_file = open("reports_file_v2.json", "w")
json.dump(js, a_file)
a_file.close()