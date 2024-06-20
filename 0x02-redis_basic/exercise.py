#!/usr/bin/env python3
"""CREATE A CACHE CLASS WITH METHODS"""
import redis
from uuid import uuid4
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def incr(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return incr


def call_history(method: Callable) -> Callable:
    """Stores history of Cache calls"""
    inputList = method.__qualname__ + ":inputs"
    outputList = method.__qualname__ + ":outputs"

    @wraps(method)
    def historyWrapper(self, *args, **kwargs):
        """Actual wrapper function"""
        self._redis.rpush(inputList, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputList, str(output))
        return output
    return historyWrapper


class Cache:
    """Cache class"""
    def __init__(self) -> None:
        """Initializer"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores a value in a new ID and returns the ID"""
        newID = str(uuid4())
        self._redis.set(newID, data)
        return newID

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """gets a value from Redis"""
        key = self._redis.get(key)
        if fn:
            return fn(key)
        return key

    def get_str(self, key: str) -> str:
        """gets a string value from Redis"""
        return self.get(key, lambda i: i.decode('UTF-8'))

    def get_int(self, key: str) -> str:
        """gets an integer value from Redis"""
        return self.get(key, lambda i: int(i))
