from flask import Blueprint, jsonify, request
from db.redis import redis_client
import requests
import os

weather_bp = Blueprint('weather', __name__, url_prefix='/third-party-service/weather')

# Set your WeatherAPI Key (ideally use environment variable for secrets)
WEATHERAPI_KEY = os.environ.get('WEATHERAPI_KEY', '0533299ca37745ffbce52129250206')
WEATHERAPI_BASE = 'http://api.weatherapi.com/v1'

def _fetch_from_weatherapi(endpoint, params):
    params['key'] = WEATHERAPI_KEY
    try:
        resp = requests.get(f"{WEATHERAPI_BASE}/{endpoint}.json", params=params, timeout=8)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {'error': str(e)}

@weather_bp.route('/current', methods=['GET'])
def current_weather():
    city = request.args.get('city', 'London')
    cache_key = f'weather:current:{city.lower()}'
    cached_weather = redis_client.get(cache_key)
    if cached_weather:
        return jsonify({'city': city, 'data': eval(cached_weather), 'source': 'redis'})

    # Fetch live weather from API
    api_data = _fetch_from_weatherapi('current', {'q': city})
    if "error" not in api_data:
        redis_client.setex(cache_key, 60*10, str(api_data))  # Cache 10 min
    return jsonify({'city': city, 'data': api_data, 'source': 'service'})

@weather_bp.route('/forecast', methods=['GET'])
def weather_forecast():
    city = request.args.get('city', 'London')
    days = request.args.get('days', 7)
    cache_key = f'weather:forecast:{city.lower()}:{days}'
    cached_forecast = redis_client.get(cache_key)
    if cached_forecast:
        return jsonify({'city': city, 'forecast': eval(cached_forecast), 'source': 'redis'})

    api_data = _fetch_from_weatherapi('forecast', {'q': city, 'days': days})
    if "error" not in api_data:
        redis_client.setex(cache_key, 60*10, str(api_data))  # Cache 10 min
    return jsonify({'city': city, 'forecast': api_data, 'source': 'service'})