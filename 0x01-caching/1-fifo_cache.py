#!/usr/bin/env python3
"""This module defines the class LIFOCache"""
from base_caching import BaseCaching
from collections import OrderedDict


class FIFOCache(BaseCaching):
    """FIFO cache system"""

    def __init__(self):
        """Initializes class attribute"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """load data into cache"""
        if key and item:
            self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_key, _ = self.cache_data.popitem(last=False)
            print(f"DISCARD: {first_key}")

    def get(self, key):
        """retrieve item in cache"""
        return self.cache_data.get(key, None)
