from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Proxy(Base):
    __tablename__ = 'proxies'

    id = Column(Integer, primary_key=True)
    ip_address = Column(String)
    port = Column(Integer)
    protocol = Column(String)
    anonymity_level = Column(String)
    country = Column(String)
    speed = Column(Float)

