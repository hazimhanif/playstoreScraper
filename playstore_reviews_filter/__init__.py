
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
import os

print(len(os.listdir("D:/")))