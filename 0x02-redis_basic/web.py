#!/usr/bin/env python3
"""Tracks and caches HTML content"""

import redis
import requests
from typing import Callable
from functools import wraps

redis_ = redis.Redis()


def counter(method: Callable) -> Callable:
    """Returns wrapper function"""
    @wraps(method)
    def wrapper(url):
        """Wrapper function"""
        redis_.incr(f"count:{url}")
        cachedResponse = redis_.get(f"cached:{url}")
        if cachedResponse:
            return cachedResponse.decode("UTF-8")
        else:
            response = method(url)
            redis_.setex(f"cached:{url}", 10, response)
            return response
    return wrapper


@counter
def getPage(url: str) -> str:
    """Get the HTML content and return text"""
    return requests.get(url).text
