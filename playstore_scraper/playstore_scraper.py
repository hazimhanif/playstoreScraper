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
from bs4 import BeautifulSoup


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
        headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
        payload = 'reviewType=0&pageNum=%d&hl=%s&id=%s&reviewSortOrder=2&xhr=1' %(pageNum,hl,appId)
        
        page_text = requests.post(url, data=payload, headers=headers).text[6:]
        js = json.loads(page_text)
        
        if(len(js[0])<3 and pageN==0):
            skipApp=True
            return(revList)
        
        if(len(js[0])<3):
            break
        
        soup = BeautifulSoup(js[0][2],"lxml")
        reviews_div = soup.find_all( 'div', {'class':'single-review'} )
        
        review_date=[]
        review_author=[]
        review_rating=[]
        review_title=[]
        review_text=[]
        for review in reviews_div:
            body = review.find(class_='review-body')
            title = body.find(class_='review-title')
            link = body.find(class_='review-link')
            date = review.find(class_='review-date')
            rating_old = review.find(class_='tiny-star').get('aria-label')
            name = review.find(class_='author-name')
            title_old=title.get_text().strip()
            title.decompose()
            link.decompose()
            text_old = body.get_text().strip()
            date_old = date.get_text()
            name_old = name.get_text().strip()
            
            review_date.append(date_old)
            review_author.append(name_old)
            review_rating.append(rating_old)
            review_title.append(title_old)
            review_text.append(text_old)
        
        if(len(review_rating)==0 and pageN==0):
            skipApp=True
            return(revList)
        
        if(len(review_rating)==0):
            break
        
        saveRawData(js[0][2],appId,pageNum)
        revsPerPage=getReviews(appSingleInfo,review_date,review_text,review_rating,review_author,review_title)
        
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
    
def getReviews(appSingleInfo,review_date,review_text,review_rating,review_author,review_title):
    global reviewsCounter
    
    rateList={"Dinilaikan 5 bintang daripada lima bintang":5,
              "Dinilaikan 4 bintang daripada lima bintang":4,
              "Dinilaikan 3 bintang daripada lima bintang":3,
              "Dinilaikan 2 bintang daripada lima bintang":2,
              "Dinilaikan 1 bintang daripada lima bintang":1,
              "Dinilaikan 0 bintang daripada lima bintang":0}
    
    c=0
    
    revPerPage=[]
    
    rev_date=""
    rev_author=""
    rev_text=""
    rev_rating=""
    rev_title=""
    
    try:
        while(c < len(review_rating)):
            rev_date=review_date[c]
            rev_author=review_author[c]
            rev_rating=rateList[review_rating[c]]
            rev_title=review_title[c]
            rev_text=review_text[c]
            
            if rev_title==" " or rev_title=="":
                rev_title="NA"
            if rev_text==" " or rev_text=="":
                rev_text="NA"
            if rev_author==" " or rev_author=="":
                rev_author="NA"
    
            revPerPage.append({'appId':appSingleInfo['appId'],'appTitle':appSingleInfo['title'],'appScore':float(appSingleInfo['appScore']),'appPrice':float(appSingleInfo['price']),'revDate': rev_date,'revAuthor':rev_author,'revRating':float(rev_rating),'revTitle':rev_title,'revText':rev_text})
            reviewsCounter+=1
            c=c+1
               
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
            json.dump(revPerApp, outfile, indent=4, sort_keys=True, separators=(',', ':'),ensure_ascii=False).encode('utf8')
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
        
        countdown(20,appList[i]['appId'],len(appList))

if __name__ =="__main__":
    main()
