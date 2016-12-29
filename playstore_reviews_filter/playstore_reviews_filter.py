# -*- coding: utf-8 -*-

'''
Created on 13 Dec 2016

@author: Hazim Hanif
'''
import os
import codecs
import json
import re

global wordList
global indonList
global finalList
global english_count
global indon_count
global total_count
global drop_count
global total_apps

total_apps=0
english_count=0
indon_count=0
total_count=0
drop_count=0
finalList=[]
revDir="D:/scraper/playstore/reviews/"
dictDir="D:/OneDrive/Documents/FSKTM/Master (Sentiment Analysis)/WordList/"
filteredDir="D:/scraper/playstore/filtered_reviews/"

def saveFinalList():
    try:
        with codecs.open("D:/scraper/playstore/final_list_clean.json", 'wb','utf-8') as outfile:
            json.dump(finalList, outfile, indent=4, sort_keys=True, separators=(',', ':'),ensure_ascii=False).encode('utf8')
    except Exception as e:
        print(e)


def addToFinalList(data):
    global finalList
    for element in data:
        finalList.append(element)
    

def saveFilteredReviews(data,file):
    filename = filteredDir+file
    try:
        with codecs.open(filename, 'wb','utf-8') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True, separators=(',', ':'),ensure_ascii=False).encode('utf8')
    except Exception as e:
        print(e)

def isIndon(wordIndo):
    
    if wordIndo in map(str.lower,[x.strip("\r\n\t") for x in indonList]):
            #print("Indo: "+wordIndo)
            return 1            
    return 0

def isEnglish(word):
    for i in range(0,len(wordList)):
        if word in map(str.lower,wordList[i]):
            #print("English: "+word)
            return 1            
    return 0
    
def getReviews(data):
    global english_count
    global indon_count
    global total_count
    global drop_count
    i=0
    size_data = len(data)
    while i < size_data:
        countEnglish_perRev=0
        countIndon_perRev=0
        words=str(data[i]['revText']).strip(".,!?:;`~@#$%^&*()-+=*'[]{}|\"/<>")
        words= re.sub("\."," ",words)
        words= re.sub("\,"," ",words)
        words= re.sub("  "," ",words)
        words= re.sub("   "," ",words)
        words=words.lower()
        words_split=words.split(sep=" ")

        for word in words_split:
            countEnglish_perRev=countEnglish_perRev+isEnglish(word)
            countIndon_perRev=countIndon_perRev+isIndon(word)
        
        if countEnglish_perRev == len(words_split):
            #print("English: "+words)
            english_count=english_count+1
            drop_count=drop_count+1
            del data[i]
            size_data=size_data-1
            continue
          
        if countIndon_perRev > (len(words_split)/2):
            #print("Endon: "+words)
            indon_count=indon_count+1
            drop_count=drop_count+1
            del data[i]
            size_data=size_data-1
            continue
        
        data[i]['revText']=words
        total_count=total_count+1
        i=i+1
    return(data)
        
def openFile(file):
    filename=revDir+file
    with codecs.open(filename,'rb','utf-8') as data_file:    
        return(json.load(data_file))

def info():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=========2-Steps Reviews Filter Info===========")
    print("Total apps: %d/%d" % (total_apps,len(os.listdir(revDir))))
    print("Total reviews: ",total_count)
    print("English reviews: ",english_count)
    print("Indon reviews: ",indon_count)
    print("Drop reviews: ",drop_count)

def loadWordList():
    global wordList
    global indonList
    indonList=[]
    wordList=[]
    
    i=0
    for file in os.listdir(dictDir):
        if(str(file)=="indon.txt"):
            continue
        
        filename=dictDir+file
        data=codecs.open(filename,'rb','utf-8')
        wordList.append(data.readlines())
        for j in range(0,len(wordList[i])):
            wordList[i][j]=str(wordList[i][j]).strip("\r\n\t")
    
        i=i+1
     
    data=codecs.open("D:/OneDrive/Documents/FSKTM/Master (Sentiment Analysis)/WordList/indon.txt",'rb','utf-8')    
    indonList=data.readlines()   
        
def main():
    global total_apps

    loadWordList()
    for file in os.listdir(revDir):
        total_apps=total_apps+1
        info()
        data=openFile(file)
        data=getReviews(data)
        saveFilteredReviews(data,file)
        addToFinalList(data)
    
    saveFinalList()

if __name__ == '__main__':
    main()