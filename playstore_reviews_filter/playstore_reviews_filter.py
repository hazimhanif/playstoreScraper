'''
Created on 13 Dec 2016

@author: Hazim Hanif
'''
import os
import codecs
import json

global wordList

revDir="D:/scraper/playstore/reviews/"
dictDir="D:/OneDrive/Documents/FSKTM/Master (Sentiment Analysis)/WordList/"

def isEnglish(word):
    countEnglish=0
    for i in range(0,len(wordList)):
        if(word in wordList[i]):
            countEnglish=countEnglish+1
            break
    print(wordList[0][0])
    
    
def getReviews(data):
    words=str(data[0]['revText']).split(sep=" ")
    for word in words:
        if 
        
        
def openFile(file):
    filename=dictDir+file
    with codecs.open(filename,'rb','utf-8') as data_file:    
        return(json.load(data_file))
    
def openWordList():
    global wordList
    wordList=[]
    
    i=0
    for file in os.listdir(dictDir):
        filename=dictDir+file
        data=codecs.open(filename,'rb','utf-8')
        wordList.append(data.readlines())
        for j in range(0,len(wordList[i])):
            wordList[i][j]=str(wordList[i][j]).strip("\r\n\t")
    
        i=i+1
    
        
def main():
    
    openWordList()
    for file in os.listdir(dictDir):
        #data=openFile(file)
        #getReviews(data)
        break
    

if __name__ == '__main__':
    main()