# coding: utf-8
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Wbalance(Base):
    __tablename__ = 'wbalance'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    totoal_in = Column(Float)
    auth_use = Column(Float)
    loss = Column(Float)
    charge_auth = Column(Float)
    uncharge_auth = Column(Float)
    charge_measure = Column(Float)
    charge_unmeasure = Column(Float)
    uncharge_measure = Column(Float)
    uncharge_unmeasure = Column(Float)
    apparent_loss = Column(Float)
    actual_loss = Column(Float)
    unauth_use = Column(Float)
    statistic_error = Column(Float)
    money_back = Column(Float)
    money_waste = Column(Float)
