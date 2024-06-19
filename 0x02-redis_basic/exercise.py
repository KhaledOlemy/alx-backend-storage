#!/usr/bin/env python3
"""CREATE A CACHE CLASS WITH METHODS"""
import redis
from uuid import uuid4
from typing import Union, Callable


class Cache:
    """Cache class"""
    def __init__(self) -> None:
        """Initializer"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
