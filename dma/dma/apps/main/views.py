from flask import Blueprint,render_template,url_for,redirect,session,request,flash
from apps import app,db

from apps.models import WBalance

from . import main



@main.route('/')
def index():
    
    return render_template('index.html')
    
@main.route('/wbalance')
def wbalance():
    return render_template('main/wbalance.html')

@main.route('/wstasitc')
def wstasitc():
    return 'adsfds'

@main.route('/wdma')
def wdma():
    balance = WBalance.query.order_by(WBalance.name).all()
    month_group = [ba.name for ba in balance ]
    return render_template('main/dma.html',balance=balance[0],month_group=month_group,current_mon=month_group[0])
    
@main.route('/wdma/<mon>')
def wdma_mon(mon):
    balance = WBalance.query.order_by(WBalance.name).all()
    month_group = [ba.name for ba in balance ]
    balance1 = WBalance.query.filter_by(name=mon).first()
    return render_template('main/dma.html',balance=balance1,month_group=month_group,current_mon=mon)
