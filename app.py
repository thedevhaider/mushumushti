#!/usr/bin/python
# -*-coding: utf-8 -*-

# import neccessary files
import requests, json
from flask import Flask, render_template, request, url_for, flash, redirect
from mongokit import Document, Connection
from datetime import datetime

# remote database url
uri = 'mongodb://amustaque97:<password>@ds129541.mlab.com:29541/portfolio'

# create Connection
connection = Connection(host=uri,
            connectTimeoutMS=30000,
            socketTimeoutMS=None,
            socketKeepAlive=True)

db = connection.portfolio
collection = db.logs

# app with the file name
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Expires'] = 0
        response.headers['Pragma'] = 'no-cache'
        return response


# generate logs details
def generate_details():
    url = 'http://ip-api.com/json/' + request.remote_addr
    r = requests.get(url)
    data = r.json()
    print(data['status'])
    if data['status'] == 'success':
        if collection.save(data):
            return True
    else :
        return False

# index page
@app.route('/')
def index():

    #  if the details are saved
    if generate_details():
        return render_template('index.htm')
    else:
        return render_template('error.htm')


# about page
@app.route('/about')
def about():
    generate_details()
    git = 'https://github.com/amustaque97'
    fb = 'https://www.facebook.com/profile.php?id=100020871090758'
    twitter = 'https://twitter.com/amustaque97'
    linkedin = 'https://www.linkedin.com/in/mustaque-ahmed/'
    return render_template('about.htm',git=git,fb=fb,twitter=twitter,linkedin=linkedin)

# skills page
@app.route('/skills')
def skills():
    generate_details()
    return render_template('skills.htm')


# run
if __name__ == '__main__':
    app.run()
