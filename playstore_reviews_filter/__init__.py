'''
Created on 13 Dec 2016

@author: Hazim Hanif

This for the 2-step filtration process of the reviews scrapped from Google Playstore
'''

import codecs
import json

with codecs.open("D:/scraper/playstore/reviews/com.imdb.mobile.json",'rb','utf-8') as data_file:    
    data = json.load(data_file)
    print(data[0]['appId'])
