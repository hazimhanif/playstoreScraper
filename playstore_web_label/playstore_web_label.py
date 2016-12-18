# -*- coding: utf-8 -*-

'''
Created on 16 Dec 2016

@author: Hazim Hanif
'''
import flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
 
app = Flask(__name__)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!"
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('Wrong password!')
    return home()
 
def main():
    print("Starting webserver")
    app.secret_key = os.urandom(12)
    app.run()

if __name__ == '__main__':
    main()