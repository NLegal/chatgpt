from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

app = Flask(__name__)
engine = create_engine('postgresql://postgres:MoonStom1@localhost:5432/proxy_checker')
Session = sessionmaker(bind=engine)

@app.route('/create_tables', methods=['POST'])
def create_tables():
    Base.metadata.create_all(bind=engine)
    return {'status': 'Tables created'}

