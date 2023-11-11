"""
Виконайте кешування результату виконання команд name: та tag: за допомогою Redis,
щоб при повторному запиті результат пошуку брався не з MongoDB бази даних, а з кешу;
"""

import redis
from redis_lru import RedisLRU


client = redis.StrictRedis(host="localhost", port=6379, password=None, db=1)
cache = RedisLRU(client)