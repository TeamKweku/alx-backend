#!/usr/bin/python3
"""
BasicCache module that inherits from BasicCaching class
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    Implement a basic caching class
    """

    def put(self, key, item):
        """
        method that adds an item to cache
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """
        method that gets the item based on the key
        """
        return self.cache_data.get(key) if key is not None else None
