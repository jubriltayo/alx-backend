#!/usr/bin/env python3
"""This module defines class MRUCache"""
from base_caching import BaseCaching
from collections import OrderedDict


class MRUCache(BaseCaching):
    """An MRU caching system"""
    def __init__(self):
        """Initializes class attributes"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """load data into cache"""
        if key and item:
            if key not in self.cache_data and\
                    len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                mru_key, _ = self.cache_data.popitem(last=False)
                print(f"DISCARD: {mru_key}")
            self.cache_data[key] = item
            # move new entry far left
            self.cache_data.move_to_end(key, last=False)

    def get(self, key):
        """retrieve item in cache"""
        if key and key in self.cache_data:
            self.cache_data.move_to_end(key, last=False)
        return self.cache_data.get(key, None)
