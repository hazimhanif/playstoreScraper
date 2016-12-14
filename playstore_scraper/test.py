# -*- coding: utf-8 -*-

'''
Created on 30 Nov 2016

@author: Hazim Hanif
'''
import os
import json
import codecs
from lxml import html
import requests


url = "https://play.google.com/store/getreviews"
pageNum=0
appId='com.hawsoft.mobile.speechtrans'
hl="ms"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
payload = 'reviewType=0&pageNum=%d&hl=%s&id=%s&reviewSortOrder=2&xhr=1' %(pageNum,hl,appId)
  
page_text = requests.post(url, data=payload, headers=headers).text
page_text_decoded=codecs.decode(page_text,'unicode_escape')
tree = html.fromstring(str(page_text_decoded))
review_date = tree.xpath('//span[@class="review-date"]/text()')
review_text = tree.xpath('//*[@class="review-body with-review-wrapper"]//text()')
review_rating = tree.xpath('//@aria-label')
review_author = tree.xpath('//span[@class="author-name"]/text()')
  
  
print(page_text_decoded)