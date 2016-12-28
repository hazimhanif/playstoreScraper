# -*- coding: utf-8 -*-
import codecs
import requests
from lxml import html
from pygrok import Grok
import json
from bs4 import BeautifulSoup




url = "https://play.google.com/store/getreviews"
pageNum=0
appId='air.com.gaetanoconsiglio.EscapePrison'
hl="ms"
headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
payload = 'reviewType=0&pageNum=%d&hl=%s&id=%s&reviewSortOrder=2&xhr=1' %(pageNum,hl,appId)
page_text = requests.post(url, data=payload, headers=headers).text[6:]
js = json.loads(page_text)

soup = BeautifulSoup(js[0][2],"lxml")
reviews_div = soup.find_all( 'div', {'class':'single-review'} )
for review in reviews_div:
    body = review.find(class_='review-body')
    title = body.find(class_='review-title')
    link = body.find(class_='review-link')
    date = review.find(class_='review-date')
    rating = review.find(class_='tiny-star').get('aria-label')
    name = review.find(class_='author-name')
    title_new=title.get_text().strip()
    title.decompose()
    link.decompose()
    text = body.get_text().strip()
    date_new = date.get_text()
    name_new = name.get_text().strip()
    
    print(date_new)
    print(name_new)
    print(rating)
    print(title_new)
    print(text)
    print("=====")


print()