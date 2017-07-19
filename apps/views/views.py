from flask import Blueprint,render_template,url_for,redirect,session,request,flash
from apps import app





@app.route('/')
def index():
    return render_template('index.html')
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404
    
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500
    
@app.errorhandler(302)
def redirect_error(e):
    return 'you acount a 302 error',302