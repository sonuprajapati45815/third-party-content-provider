import json

from flask import Blueprint, jsonify, request
from db.redis import redis_client
from news.news_service import get_news_by_query, get_news_by_top_headline

news_bp = Blueprint('news', __name__, url_prefix='/third-party-service/news')

@news_bp.route('/latest', methods=['GET'])
def get_news_by_query_view():
    query = request.args.get('query', 'indian politics and business')
    cached_news = redis_client.get(f'news:latest{query}')
    if cached_news:
        return jsonify(json.loads(cached_news)), 200
    latest_news = get_news_by_query(query)
    redis_client.set('news:latest', json.dumps(latest_news), ex=3600)
    return latest_news, 200

@news_bp.route('/top_headline', methods=['GET'])
def top_headline():
    category = request.args.get('category', 'politics')
    country = request.args.get('country', 'india')
    cached_news = redis_client.get('top_headline:category:{}:country:{}'.format(category, country))
    if cached_news:
        return jsonify(json.loads(cached_news)), 200
    top_headline = get_news_by_top_headline(country, category)
    redis_client.set('news:latest', json.dumps(top_headline), ex=3600)
    return top_headline, 200




