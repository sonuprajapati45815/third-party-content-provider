import json

from flask import Blueprint, jsonify, request
from db.redis import redis_client
import requests
import os

weather_bp = Blueprint('weather', __name__, url_prefix='/third-party-service/weather')

# Set your WeatherAPI Key (ideally use environment variable for secrets)
WEATHERAPI_KEY = os.environ.get('WEATHERAPI_KEY', '0533299ca37745ffbce52129250206')
WEATHERAPI_BASE = 'http://api.weatherapi.com/v1'


_weather_back_images = {
  "Sunny": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80",
  "Clear": "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=1200&q=80",
  "Partly cloudy": "https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=1200&q=80",
  "Cloudy": "https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=1200&q=80",
  "Overcast": "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1200&q=80",
  "Mist": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1200&q=80",
  "Patchy rain possible": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?auto=format&fit=crop&w=1200&q=80",
  "Patchy snow possible": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80",
  "Patchy sleet possible": "https://images.unsplash.com/photo-1457269449834-928af64c684d?auto=format&fit=crop&w=1200&q=80",
  "Patchy freezing drizzle possible": "https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=1200&q=80",
  "Thundery outbreaks possible": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80",
  "Blowing snow": "https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=1200&q=80",
  "Blizzard": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80",
  "Fog": "https://images.unsplash.com/photo-1465101178521-c1a9136a3cfb?auto=format&fit=crop&w=1200&q=80",
  "Freezing fog": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1200&q=80",
  "Patchy light drizzle": "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=1200&q=80",
  "Light drizzle": "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=1200&q=80",
  "Freezing drizzle": "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=1200&q=80",
  "Heavy freezing drizzle": "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=1200&q=80",
  "Patchy light rain": "https://images.unsplash.com/photo-1444065381814-865dc9da92c0?auto=format&fit=crop&w=1200&q=80",
  "Light rain": "https://images.unsplash.com/photo-1444065381814-865dc9da92c0?auto=format&fit=crop&w=1200&q=80",
  "Moderate rain at times": "https://images.unsplash.com/photo-1465101178521-c1a9136a3cfb?auto=format&fit=crop&w=1200&q=80",
  "Moderate rain": "https://images.unsplash.com/photo-1465101178521-c1a9136a3cfb?auto=format&fit=crop&w=1200&q=80",
  "Heavy rain at times": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?auto=format&fit=crop&w=1200&q=80",
  "Heavy rain": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?auto=format&fit=crop&w=1200&q=80",
  "Light freezing rain": "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=1200&q=80",
  "Moderate or heavy freezing rain": "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=1200&q=80",
  "Light sleet": "https://images.unsplash.com/photo-1457269449834-928af64c684d?auto=format&fit=crop&w=1200&q=80",
  "Moderate or heavy sleet": "https://images.unsplash.com/photo-1457269449834-928af64c684d?auto=format&fit=crop&w=1200&q=80",
  "Patchy light snow": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80",
  "Light snow": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80",
  "Patchy moderate snow": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80",
  "Moderate snow": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80",
  "Patchy heavy snow": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80",
  "Heavy snow": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80",
  "Ice pellets": "https://images.unsplash.com/photo-1457269449834-928af64c684d?auto=format&fit=crop&w=1200&q=80",
  "Light rain shower": "https://images.unsplash.com/photo-1444065381814-865dc9da92c0?auto=format&fit=crop&w=1200&q=80",
  "Moderate or heavy rain shower": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?auto=format&fit=crop&w=1200&q=80",
  "Torrential rain shower": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?auto=format&fit=crop&w=1200&q=80",
  "Light sleet showers": "https://images.unsplash.com/photo-1457269449834-928af64c684d?auto=format&fit=crop&w=1200&q=80",
  "Moderate or heavy sleet showers": "https://images.unsplash.com/photo-1457269449834-928af64c684d?auto=format&fit=crop&w=1200&q=80",
  "Light snow showers": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80",
  "Moderate or heavy snow showers": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80",
  "Light showers of ice pellets": "https://images.unsplash.com/photo-1457269449834-928af64c684d?auto=format&fit=crop&w=1200&q=80",
  "Moderate or heavy showers of ice pellets": "https://images.unsplash.com/photo-1457269449834-928af64c684d?auto=format&fit=crop&w=1200&q=80",
  "Patchy light rain with thunder": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80",
  "Moderate or heavy rain with thunder": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80",
  "Patchy light snow with thunder": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80",
  "Moderate or heavy snow with thunder": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80"
}

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
    data = {
        'location': api_data.get('location', {}),
        "tempC": api_data.get('current', {}).get('temp_c', 0),
        "tempF": api_data.get('current', {}).get('temp_f', 0),
        "conditionText": api_data.get('current', {}).get('condition', {}).get('text'),
        "conditionIcon": api_data.get('current', {}).get('condition', {}).get('icon'),
        "bgImageUrl": _weather_back_images[api_data.get('current', {}).get('condition', {}).get('text', 'Sunny')],
        "humidity": api_data.get('current', {}).get('humidity', 0),
        "windKph": api_data.get('current', {}).get('wind_kph', 0.0),
        "windMph": api_data.get('current', {}).get('wind_mph', 0.0)
    }
    redis_client.setex(cache_key, 60 * 10, str(data))
    return jsonify({'city': city, 'data': data, 'source': 'service'})

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