import json 

f = open('articles.json')

js = json.load(f)['articles']

v = 0
r = 0
for i in js:
    i['articleId'] = v
    for rp in i ['reports']:
        rp['reportId'] = r
        r+= 1
    # print(i)
    v+= 1


a_file = open("sample_file.json", "w")
json.dump(js, a_file)
a_file.close()