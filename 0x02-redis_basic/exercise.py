#!/usr/bin/env python3
"""CREATE A CACHE CLASS WITH METHODS"""
import redis
from uuid import uuid4
from typing import Union


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
