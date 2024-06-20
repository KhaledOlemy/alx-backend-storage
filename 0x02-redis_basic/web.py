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
        tempResponse = myRedis.get(f"cached-response:{url}")
        if tempResponse:
            return tempResponse.decode("UTF-8")
        else:
            tempResponse = method(url)
            myRedis.setex(f"cached-response:{url}", 10, tempResponse)
            return tempResponse
    return methodWrapper


@counter
def getPage(url: str) -> str:
    """Get the HTML content and return text"""
    return requests.get(url).text
