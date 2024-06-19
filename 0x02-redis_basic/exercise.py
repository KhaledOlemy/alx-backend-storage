#!/usr/bin/env python3
"""CREATE A CACHE CLASS WITH METHODS"""
import redis
from uuid import uuid4

class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: str | int | float | bytes) -> str:
        newID = str(uuid4())
        self._redis.set(newID, data)
        return newID
