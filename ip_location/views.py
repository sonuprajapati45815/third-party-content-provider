import json
import requests
from flask import Blueprint, jsonify, request


ip_location_bp = Blueprint('news', __name__, url_prefix='/third-party-service/location')

@ip_location_bp.route('/byIp', methods=['GET'])
def get_news_by_query_view():
    ip_address = request.args.get('ip-address')
    url = f'http://ip-api.com/json/{ip_address}'
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        return {'status': 'error'}, 500


