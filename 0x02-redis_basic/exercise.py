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


def replay(method: Callable) -> None:
    """Replays all history of a method | gets the whole history stored"""
    qname = method.__qualname__
    cache = redis.Redis()
    fCalls = cache.get(qname).decode("UTF-8")
    fInputs = cache.lrange(f"{qname}:inputs", 0, -1)
    fOutputs = cache.lrange(f"{qname}:outputs", 0, -1)
    print(f"{qname} was called {fCalls} times:")
    for i, j in zip(fInputs, fOutputs):
        print("{}(*{}) -> {}".format(qname, i.decode('UTF-8'),
                                     j.decode('UTF-8')))


class Cache:
    """Cache class that will include all functions wrapped as instructed"""
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
