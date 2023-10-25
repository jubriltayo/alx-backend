#!/usr/bin/env python3
"""This module defines the class LIFOCache"""
from base_caching import BaseCaching
from collections import OrderedDict


class LIFOCache(BaseCaching):
    """LIFO cache system"""

    def __init__(self):
        """Initializes class attribute"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """load data into cache"""
        if key and item:
            if key not in self.cache_data and\
                    len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                last_key, _ = self.cache_data.popitem()
                print(f"DISCARD: {last_key}")
            self.cache_data[key] = item
            self.cache_data.move_to_end(key, last=True)

    def get(self, key):
        """retrieve item in cache"""
        return self.cache_data.get(key, None)
