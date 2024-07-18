#!/usr/bin/env python3
"""
Implement a get_page function
"""

import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
"""
Redis instance for module.
"""


def data_cacher(method: Callable) -> Callable:
    """
    Output of fetched data is cached
    """
    @wraps(method)
    def invoker(url) -> str:
        """
        The wrapper method for caching
        """
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL
    """
    return requests.get(url).text
