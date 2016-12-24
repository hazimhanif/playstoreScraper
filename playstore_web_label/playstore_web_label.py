# -*- coding: utf-8 -*-

'''
Created on 16 Dec 2016

@author: Hazim Hanif
'''
import os

from flask import Flask, flash, redirect, render_template, request, session, abort
import flask
import pymysql
import dbase_stuff as dbs

global nameIncoming
global revId

app = Flask(__name__)
nameIncoming=""
revId=0

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return main_screen(nameIncoming)
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    global nameIncoming
    user=dbs.login(request.form['username'])
    if request.form['password'] == user[1] and request.form['username'] == user[0]:
        session['logged_in'] = True
        nameIncoming=request.form['username']
    else:
        flash('Wrong password!')
    return home()

@app.route('/result', methods=['POST'])
def result():
    global revId
    
    addLabel(request.form['sentiment'],request.form['authenticity'],request.form['rating'])
    revdrop=dbs.getTotalReviewsDrop(nameIncoming)
    review=dbs.getReview()
    revId=review[0]
    dbs.revLock(revId)
    return render_template('main.html',revdrop=revdrop,review=review,nameIncoming=nameIncoming)

@app.route('/drop')
def drop():
    global revId
    
    dbs.setDrop(nameIncoming,revId)
    dbs.addDropsCount(nameIncoming)
    revdrop=dbs.getTotalReviewsDrop(nameIncoming)
    review=dbs.getReview()
    revId=review[0]
    dbs.revLock(revId)
    return render_template('main.html',revdrop=revdrop,review=review,nameIncoming=nameIncoming)

@app.route('/main', methods=['POST'])
def main_screen(nameIncoming):
    global revId
    
    revdrop=dbs.getTotalReviewsDrop(nameIncoming)
    review=dbs.getReview()
    revId=review[0]
    dbs.revLock(revId)
    return render_template('main.html',revdrop=revdrop,review=review,nameIncoming=nameIncoming)

def addLabel(sentiment,authenticity,rating):
    global revId
    
    print("Add Label")
    dbs.setLabel(sentiment,authenticity,rating,nameIncoming,revId)
    dbs.addReviewsCount(nameIncoming)
    revdrop=dbs.getTotalReviewsDrop(nameIncoming)
    review=dbs.getReview()
    revId=review[0]
    dbs.revLock(revId)
    return render_template('main.html',revdrop=revdrop,review=review,nameIncoming=nameIncoming)

@app.errorhandler(400)
def page_not_found(e):
    return render_template('error_400.html'),400

@app.route("/logout")
def logout():
    dbs.revUnlock(revId)
    session['logged_in'] = False
    return home()
 
def main():
    print("Preparing connection to database...")
    dbs.prepare_Database()
    print("Starting webserver...")
    app.secret_key = os.urandom(12)
    app.run()

if __name__ == '__main__':
    main()