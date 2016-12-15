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

revDir="D:/scraper/playstore/reviews/"
dictDir="D:/OneDrive/Documents/FSKTM/Master (Sentiment Analysis)/WordList/"

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
    i=0
    size_data = len(data[i])
    print(size_data)
    while i < size_data:
        countEnglish_perRev=0
        countIndon_perRev=0
        words=str(data[i]['revText']).strip(".,!?:;`~@#$%^&*()-+=*'[]{}|\"/<>\\")
        words= re.sub("\."," ",words)
        words=words.lower()
        words_split=words.split(sep=" ")
        print(words)
        print(i)

        for word in words_split:
            countEnglish_perRev=countEnglish_perRev+isEnglish(word)
            countIndon_perRev=countIndon_perRev+isIndon(word)
        
        if countEnglish_perRev == len(words_split):
            #print(words)
            #print(len(words_split))
            del data[i]
            size_data=size_data-1
            continue
        
        if countIndon_perRev > (len(words)/2):
            del data[i]
            size_data=size_data-1
            continue
        
       
        i=i+1
    return(data)
        
def openFile(file):
    filename=revDir+file
    with codecs.open(filename,'rb','utf-8') as data_file:    
        return(json.load(data_file))
    
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
    
    loadWordList()
    for file in os.listdir(revDir):
        data=openFile(file)
        print(len(data))
        data=getReviews(data)
        print(len(data))
        break
    

if __name__ == '__main__':
    main()