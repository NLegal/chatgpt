import requests
import time

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from flask import Flask, jsonify

engine = create_engine('postgresql://postgres:password@db:5432/db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Proxy(Base):
    __tablename__ = 'proxies'

    id = Column(Integer, primary_key=True)
    ip_address = Column(String)
    port = Column(Integer)
    created_at = Column(DateTime, default=time.time)

def check_proxy(proxy):
    try:
        proxies = {'http': f'http://{proxy.ip_address}:{proxy.port}', 'https': f'https://{proxy.ip_address}:{proxy.port}'}
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
        if response.ok:
            return True
    except:
        pass
    return False

app = Flask(__name__)

@app.route('/health')
def health_check():
    return jsonify({'status': 'ok'})

@app.route('/check')
def check_proxies():
    session = Session()
    proxies = session.query(Proxy).all()
    results = {}
    for proxy in proxies:
        if check_proxy(proxy):
            results[f'{proxy.ip_address}:{proxy.port}'] = True
        else:
            results[f'{proxy.ip_address}:{proxy.port}'] = False
    return jsonify(results)

if __name__ == '__main__':
    app.run()

