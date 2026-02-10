import redis
import os
redis_client = None

def init_redis():
    global redis_client
    redis_client = redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6380)),
        db=0
    )

init_redis()