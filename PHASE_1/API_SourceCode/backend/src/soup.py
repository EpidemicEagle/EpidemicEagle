from bs4 import BeautifulSoup as bs
import requests as rq

url="https://www.who.int/emergencies/disease-outbreak-news/item/2020-DON282"

res = rq.get(url)

soup = bs(res.content, features="lxml")
for link in soup.findAll('p'):
    if link != 'None':
        print(link.string)