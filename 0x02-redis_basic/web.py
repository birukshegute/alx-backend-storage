#!/usr/bin/env python3
"""
Implement a get_page function
"""

import redis
import requests
from functools import wraps
from typing import Callable


def track_get_page(method: Callable) -> Callable:
    """
    Tracks get_page
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Tracks how many times get_page is called
        """
        client = redis.Redis()
        client.incr(f'count:{url}')
        cached_page = client.get(f'{url}')
        if cached_page:
            return cached_page.decode('utf-8')
        response = fn(url)
        client.set(f'{url}', response, 10)
        return response
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL
    """
    response = requests.get(url)
    return response.text
