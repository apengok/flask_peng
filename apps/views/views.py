from flask import Blueprint,render_template,url_for,redirect,session,request,flash
from apps import app





@app.route('/')
def index():
    return render_template('index.html')