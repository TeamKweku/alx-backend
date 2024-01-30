#!/usr/bin/python3
"""
Module that implements a LIFO caching mechanism
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """LIFOCache inherits from BaseCaching.
    This caching system uses a LIFO algorithm.
    """

    def __init__(self):
        """Initialize and call the parent init."""
        super().__init__()
        self.keys = []

    def put(self, key, item):
        """
        Adding an item in the cache using the LIFO algorithm
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.keys.remove(key)
            elif len(self.keys) == BaseCaching.MAX_ITEMS:
                discarded_key = self.keys.pop()
                del self.cache_data[discarded_key]
                print("DISCARD: {}".format(discarded_key))
            self.cache_data[key] = item
            self.keys.append(key)

    def get(self, key):
        """
        Return the value in self.cache_data linked to key
        """
        return self.cache_data.get(key) if key is not None else None
