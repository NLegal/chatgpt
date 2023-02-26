from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Proxy
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
engine = create_engine('postgresql://postgres:MoonStorm1@localhost:5432/proxy_checker')
Session = sessionmaker(bind=engine)

@app.route('/filter_proxies', methods=['GET'])
def filter_proxies():
    # parse query parameters
    country = request.args.get('country')
    protocol = request.args.get('protocol')
    anonymity_level = request.args.get('anonymity_level')
    sort_by = request.args.get('sort_by')
    limit = request.args.get('limit', 100)

    # build query
    session = Session()
    query = session.query(Proxy)

    if country:
        query = query.filter_by(country=country)

    if protocol:
        query = query.filter_by(protocol=protocol)

    if anonymity_level:
        query = query.filter_by(anonymity_level=anonymity_level)

    if sort_by:
        if sort_by == 'speed':
            query = query.order_by(Proxy.speed)
        elif sort_by == 'country':
            query = query.order_by(Proxy.country)
        elif sort_by == 'port':
            query = query.order_by(Proxy.port)
        elif sort_by == 'protocol':
            query = query.order_by(Proxy.protocol)
        elif sort_by == 'anonymity_level':
            query = query.order_by(Proxy.anonymity_level)

    # execute query asynchronously using multi-threading
    with ThreadPoolExecutor() as executor:
        future = executor.submit(query.limit(limit).all)

    # serialize response
    results = []
    for proxy in future.result():
        results.append({
            'ip_address': proxy.ip_address,
            'port': proxy.port,
            'protocol': proxy.protocol,
            'anonymity_level': proxy.anonymity_level,
            'country': proxy.country,
            'speed': proxy.speed
        })

    return jsonify(results)

