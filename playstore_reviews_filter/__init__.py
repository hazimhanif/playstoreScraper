'''
Created on 13 Dec 2016

@author: Hazim Hanif

This for the 2-step filtration process of the reviews scrapped from Google Playstore
'''

import codecs
import json
import re


with codecs.open("D:/scraper/playstore/reviews/com.imdb.mobile.json",'rb','utf-8') as data_file:    
    data = json.load(data_file)

data=codecs.open("D:/OneDrive/Documents/FSKTM/Master (Sentiment Analysis)/WordList/indon.txt",'rb','utf-8')    
indonList=data.readlines()
for wordIndo in [z.strip("\r\n\t") for z in indonList]:
    print(wordIndo)
