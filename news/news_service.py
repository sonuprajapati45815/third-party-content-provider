import os
import requests

##news api
API_KEY = os.getenv("NEWS_API_KEY", "c1a233d12a44416c84076894d3ed02e1")
NEWS_QUERY_ENDPOINT_1 = f'''https://newsapi.org/v2/everything?q=QUERY&sortBy=popularity&apiKey={API_KEY}'''
NEWS_COUNTRY_ENDPOINT_1 = f'''https://newsapi.org/v2/top-headlines?country=COUNTRY&category=CATEGORY&apiKey={API_KEY}'''

def get_news_by_query(query):
    url = NEWS_QUERY_ENDPOINT_1.replace("QUERY", query)
    print(url)
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_news_by_top_headline(country, category):
    url = NEWS_COUNTRY_ENDPOINT_1.replace("COUNTRY", country).replace("CATEGORY", category)
    print(url)
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        return []