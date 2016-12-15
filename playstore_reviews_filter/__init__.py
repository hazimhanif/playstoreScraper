
'''
Created on 13 Dec 2016

@author: Hazim Hanif

This for the 2-step filtration process of the reviews scrapped from Google Playstore
'''

import codecs
import json
import re
import requests
from lxml import html

a=[]

b=[{
        "appId":"aero.sita.lab.resmobileweb.android.mh",
        "appPrice":0.0,
        "appScore":4.0,
        "appTitle":"Malaysia Airlines",
        "revAuthor":"Siti Sumaini Siti Sumaini",
        "revDate":"7 Ogos 2016",
        "revRating":5.0,
        "revText":"Yang terbaik",
        "revTitle":"Malaysia airlines"
    },
    {
        "appId":"aero.sita.lab.resmobileweb.android.mh",
        "appPrice":0.0,
        "appScore":4.0,
        "appTitle":"Malaysia Airlines",
        "revAuthor":"Nur Ain",
        "revDate":"30 Jun 2015",
        "revRating":5.0,
        "revText":"Suka",
        "revTitle":"Layanan sangat bagus"
    }]

for x in b:
    a.append(x)
print(a[0])
print(a[1])
print(a)
