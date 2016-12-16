'''
Created on 16 Dec 2016

@author: Hazim Hanif
'''
from flask import Flask
app = Flask(__name__)
 
@app.route("/")
def hello():
    return "Hello World!"
   
def main():
    print("Starting webserver")
    app.run()

if __name__ == '__main__':
    main()