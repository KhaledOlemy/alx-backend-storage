#!/usr/bin/env python3
"""Tracks and caches HTML content"""

import redis
import requests
from typing import Callable
from functools import wraps

myRedis = redis.Redis()


def counter(method: Callable) -> Callable:
    """Returns wrapper function"""

    @wraps(method)
    def methodWrapper(url):
        """Wrapper function"""
        myRedis.incr(f"count:{url}")
        cachedResponse = myRedis.get(f"cached-response:{url}")
        if cachedResponse:
            return cachedResponse.decode("UTF-8")
        else:
            response = method(url)
            myRedis.setex(f"cached-response:{url}", 10, response)
            return response
    return methodWrapper


@counter
def getPage(url: str) -> str:
    """Get the HTML content and return text"""
    return requests.get(url).text
