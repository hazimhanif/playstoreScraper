# -*- coding: utf-8 -*-

'''
Created on 22 Dec 2016

@author: Hazim Hanif
'''
import pymysql

global db
global cursor

cursor=None
db=None

def prepare_Database():
    global db
    global cursor
    db = pymysql.connect(host="127.0.0.1",user="",passwd="",db="test",port=3306)
    cursor=db.cursor()
    
def logout():
    global db
    db.close()

def login(nameIncoming):
    db.commit()
    sql = "SELECT * FROM user where username='%s'" % (nameIncoming)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        result = cursor.fetchone()
        if(result is None):
            return([None,None,None,None])
        else:
            uname = result[1]
            pwd = result[2]
            return([uname,pwd])
    except:
        print ("Error: login")
        

def getTotalReviewsDrop(nameIncoming):
    result=[]
    sql1 = "SELECT COUNT(*) FROM playstore WHERE labeller_name='%s' AND label_drop IS NULL" % (nameIncoming)
    sql2 = "SELECT COUNT(*) FROM playstore WHERE labeller_name='%s' AND label_drop IS NOT NULL" % (nameIncoming)
    try:
        cursor.execute(sql1)
        result.append(str(cursor.fetchone()).strip(',\(\)'))
        cursor.execute(sql2)
        result.append(str(cursor.fetchone()).strip(',\(\)'))
        return result
    except:
        print ("Error: getTotalReviewsDrop")
        

def addReviewsCount(nameIncoming):
    sql = "UPDATE user SET total_review=total_review+1 WHERE username='%s'" % (nameIncoming)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: addReviewsCount")
        
        
def getReview(nameIncoming):
    sql="SELECT id,appId,appPrice,appScore,appTitle,revAuthor,revDate,revRating,revText,revTitle FROM playstore WHERE revlock=1 AND name_revLock='%s' AND labeller_name IS NULL LIMIT 1" % (nameIncoming)
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        if(result is None):
            None
        else:
            return result
    except:
        print ("Error: getReview")
        
    sql="SELECT id,appId,appPrice,appScore,appTitle,revAuthor,revDate,revRating,revText,revTitle FROM playstore WHERE revlock=0 AND labeller_name IS NULL LIMIT 1"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result
    except:
        print ("Error: getReview")
        

#def setLabel_old(sentiment,authenticity,rating,nameIncoming,revId):
#    sql="UPDATE playstore SET label_sentiment='%s',label_authenticity='%s',label_rating=%f,labeller_name='%s' WHERE id=%d" % (sentiment,authenticity,float(rating),nameIncoming,revId)
#    try:
#        cursor.execute(sql)
#        db.commit()
#    except:
#        print ("Error: setLabel")

def setLabel(sentiment,authenticity,nameIncoming,revId):
    sql="UPDATE playstore SET label_sentiment='%s',label_authenticity='%s',label_rating=NULL,labeller_name='%s' WHERE id=%d" % (authenticity,nameIncoming,revId)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: setLabel")

def setDrop(nameIncoming,revId):
    sql="UPDATE playstore SET label_drop='Drop',labeller_name='%s' WHERE id=%d" % (nameIncoming,revId)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: setDrop")
        
def revLock(nameIncoming,revId):
    sql = "UPDATE playstore SET revLock=1,name_revLock='%s' WHERE id=%d" % (nameIncoming,revId)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: revLock")

def revUnlock(revId):
    sql = "UPDATE playstore SET revLock=0,name_revLock=NULL WHERE id=%d" % (revId)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: revUnlock")
