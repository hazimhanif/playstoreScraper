# -*- coding: utf-8 -*-

'''
Created on 16 Dec 2016

@author: Hazim Hanif
'''
import flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
 
app = Flask(__name__)

test = {
        "appId":"aero.sita.lab.resmobileweb.android.mh",
        "appPrice":0.0,
        "appScore":4.0,
        "appTitle":"Malaysia Airlines",
        "revAuthor":"Siti Sumaini Siti Sumaini",
        "revDate":"7 Ogos 2016",
        "revRating":5.0,
        "revText":"yang terbaik",
        "revTitle":"Malaysia airlines"
    }


 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return main_screen()
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('Wrong password!')
    return home()

@app.route('/result', methods=['POST'])
def result():
    print(request.form['sentiment'])
    print(request.form['authenticity'])
    print(request.form['rating'])
    
    return render_template('main.html',test=test)

@app.route('/main', methods=['POST'])
def main_screen():
    return render_template('main.html',test=test)

 
def main():
    print("Starting webserver")
    app.secret_key = os.urandom(12)
    app.run()

if __name__ == '__main__':
    main()