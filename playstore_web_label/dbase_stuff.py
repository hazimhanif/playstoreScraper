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
    db = pymysql.connect("localhost","username","password","test" )
    cursor=db.cursor()

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
            t_review = result[3]
            t_drop = result[4]
            return([uname,pwd,t_review,t_drop])
    except:
        print ("Error: unable to fecth data")
        

def getTotalReviewsDrop(nameIncoming):
    sql = "SELECT total_review,total_drop FROM user WHERE username='%s'" % (nameIncoming)
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result
    except:
        print ("Error: unable to fecth data")
        

def addReviewsCount(nameIncoming):
    sql = "UPDATE user SET total_review=total_review+1 WHERE username='%s'" % (nameIncoming)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: unable to fecth data")

def addDropsCount(nameIncoming):
    sql = "UPDATE user SET total_drop=total_drop+1 WHERE username='%s'" % (nameIncoming)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: unable to fecth data")
        
        
def getReview(nameIncoming):
    sql="SELECT id,appId,appPrice,appScore,appTitle,revAuthor,revDate,revRating,revText,revTitle FROM playstore1 WHERE revlock=1 AND name_revLock='%s' AND labeller_name IS NULL LIMIT 1" % (nameIncoming)
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        if(result is None):
            None
        else:
            return result
    except:
        print ("Error: unable to fecth data")
        
    sql="SELECT id,appId,appPrice,appScore,appTitle,revAuthor,revDate,revRating,revText,revTitle FROM playstore1 WHERE revlock=0 AND labeller_name IS NULL LIMIT 1"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result
    except:
        print ("Error: unable to fecth data")
        
def setLabel(sentiment,authenticity,rating,nameIncoming,revId):
    sql="UPDATE playstore1 SET label_sentiment='%s',label_authenticity='%s',label_rating=%f,labeller_name='%s' WHERE id=%d" % (sentiment,authenticity,float(rating),nameIncoming,revId)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: unable to fecth data")

def setDrop(nameIncoming,revId):
    sql="UPDATE playstore1 SET label_drop='Drop',labeller_name='%s' WHERE id=%d" % (nameIncoming,revId)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: unable to fecth data")
        
def revLock(nameIncoming,revId):
    sql = "UPDATE playstore1 SET revLock=1,name_revLock='%s' WHERE id=%d" % (nameIncoming,revId)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: unable to fecth data")

def revUnlock(revId):
    sql = "UPDATE playstore1 SET revLock=0,name_revLock=NULL WHERE id=%d" % (revId)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: unable to fecth data")