# -*- coding: utf-8 -*-

'''
Created on 1 Dec 2016

@author: Hazim Hanif
'''

import requests
import codecs
import os
import time
from lxml import html
import json

global reviewsCounter
global appsCounter
global skipApp
global currentApps

skipApp=False
reviewsCounter=0
appsCounter=0
def saveRawData(raw_data,appId,pageNum):
    
    filename = "D:/scraper/playstore/raw/reviews_%s_page_%d.raw" % (appId,pageNum)
    try:
        fopen = codecs.open(filename,"wb","utf-8")
        fopen.write(raw_data)
    except Exception as e:
        print(e)

def sendRequest(appSingleInfo):
    global skipApp
    
    skipApp=False
    pageN=0
    revList=[]
    sleeptime=[10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
    
    
    while(True):
        url = "https://play.google.com/store/getreviews"
        pageNum=pageN
        appId=appSingleInfo['appId']
        hl="ms"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = 'reviewType=0&pageNum=%d&hl=%s&id=%s&reviewSortOrder=2&xhr=1' %(pageNum,hl,appId)
        
        page_text = requests.post(url, data=payload, headers=headers).text
        page_text_decoded=codecs.decode(page_text,'unicode_escape')
        tree = html.fromstring(page_text_decoded)
        review_date = tree.xpath('//span[@class="review-date"]/text()')
        review_text = tree.xpath('//*[@class="review-body with-review-wrapper"]//text()')
        review_rating = tree.xpath('//@aria-label')
        review_author = tree.xpath('//span[@class="author-name"]/text()')
        
        
        if(review_rating.__len__()==0 and pageN==0):
            skipApp=True
            return(revList)
        
        if(review_rating.__len__()==0):
            break
        
        saveRawData(page_text_decoded,appId,pageNum)
        revsPerPage=getReviews(appSingleInfo,review_date,review_text,review_rating,review_author)
        
        try:
            while(True):
                revList.append(revsPerPage.pop())
        except:
            None
    
        pageN+=1
        
        if pageN in sleeptime:
            for i in range(60,0,-1):
                print('\nNow sleeping for',i,' seconds because its already page ',pageN)
                time.sleep(1)
                os.system('cls' if os.name == 'nt' else 'clear')
    
    return(revList)
        
def readAppList():
    global appTotal
    global appCount
    
    appList=[]
    
    catList=os.listdir("D:/scraper/playstore/applist")
    appTotal=len(catList)
    
    for i in range(0,appTotal):
        try:
            filename = "D:/scraper/playstore/applist/%s" % (catList[i])
            fopen = codecs.open(filename,"rb", "utf-8")
        except Exception as e:
            print(e)
        
        k= list(fopen.readlines(99999))
        c=0
        while(c<len(k)):
            Url=k[c].split(sep='\'')[1]
            AppId=k[c+1].split(sep='\'')[1]
            Title=k[c+2].split(sep='\'')[1]
            Summary=k[c+3].split(sep='\'')[1]
            Developer=k[c+4].split(sep='\'')[1]
            Icon=k[c+5].split(sep='\'')[1]
            Score=(k[c+6].split(sep=' ')[5]).strip('\n|,')
            Price=k[c+7].split(sep='\'')[1]
            Free=k[c+8].split(sep=' ')[5]
    
            
            appList.append({'appId':AppId,'title':Title,'appScore':float(Score),'price':float(Price)})
            c=c+9
    
    return appList
    
def getReviews(appSingleInfo,review_date,review_text,review_rating,review_author):
    global reviewsCounter
    
    rateList={"Dinilaikan 5 bintang daripada lima bintang":5,
              "Dinilaikan 4 bintang daripada lima bintang":4,
              "Dinilaikan 3 bintang daripada lima bintang":3,
              "Dinilaikan 2 bintang daripada lima bintang":2,
              "Dinilaikan 1 bintang daripada lima bintang":1,
              "Dinilaikan 0 bintang daripada lima bintang":0}
    
    i=1
    c=0
    
    revPerPage=[]
    
    rev_date=""
    rev_author=""
    rev_text=""
    rev_rating=""
    rev_title=""
    
    try:
        while(True):
            rev_date=review_date[c]
            rev_author=review_author[c]
            rev_rating=review_rating[c]
            
            if review_text[i+1] !=" ":
                rev_title=review_text[i]
                rev_text=review_text[i+1]
                i=i+7
            else:
                rev_title="Undefined"
                rev_text= review_text[i]
                i=i+6
            c=c+1
            
            rev_rating=rateList[rev_rating]
            rev_author=rev_author[2:-1]
            rev_text=rev_text[1:-1]
            
            revPerPage.append({'appId':appSingleInfo['appId'],'appTitle':appSingleInfo['title'],'appScore':float(appSingleInfo['appScore']),'appPrice':float(appSingleInfo['price']),'revDate': rev_date,'revAuthor':rev_author,'revRating':float(rev_rating),'revTitle':rev_title,'revText':rev_text})
            reviewsCounter+=1
            
    except Exception as e:
        None
    
    return(revPerPage)

def checkTotalReviews():
    global reviewsCounter
    global currentApps
    currentApps = os.listdir("D:/scraper/playstore/reviews/")
    for file in currentApps:
        filename="D:/scraper/playstore/reviews/%s" %file
        with codecs.open(filename,'rb','utf-8') as data_file:    
            data = json.load(data_file)
            reviewsCounter=reviewsCounter+len(data)
            
def checkAppAvailability(appId):
    global appsCounter
    new_name = "%s.json" % appId
    if new_name in currentApps:
        appsCounter=appsCounter+1
        return(True)
    else:
        return(False)

def saveRevToFile(appId,revPerApp):

    filename = "D:/scraper/playstore/reviews/%s.json" % (appId)
    try:
        with codecs.open(filename, 'wb','utf-8') as outfile:
            json.dump(revPerApp, outfile, indent=4, sort_keys=True, separators=(',', ':'))
    except Exception as e:
        print(e)

def countdown(t,appId,totalApps): # in seconds
    for i in range(t,0,-1):
            print("======Playstore scraper 0.1========")
            print("Apps Count: ",appsCounter,"/",totalApps)
            print("Reviews count: ",reviewsCounter)
            print("Finished fetching reviews for: ",appId)
            print('\nNow sleeping for',i,' seconds')
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')

def main():
    global appsCounter
    skipCount=0
    
    print("======Playstore scraper 0.1========")
    print("Fetching app list...")
    
    appList=readAppList()
    checkTotalReviews()
    
    
    for i in range(0,len(appList)):
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("======Playstore scraper 0.1========")
        print("Apps Count: ",appsCounter,"/",len(appList))
        print("Apps Skipped: ",skipCount)
        print("Reviews count: ",reviewsCounter)
        print("Fetching reviews for: ",appList[i]['appId'])
        
        availability=checkAppAvailability(appList[i]['appId'])
        
        if(availability==True):
            continue
        
        revPerApp=sendRequest(appList[i])
                
        if(skipApp==True):
            skipCount=skipCount+1
            continue
        
        saveRevToFile(appList[i]['appId'],revPerApp)
        appsCounter+=1
        
        countdown(60,appList[i]['appId'],len(appList))

if __name__ =="__main__":
    main()
