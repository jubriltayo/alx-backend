#!/usr/bin/python3
"""This module defines class BasicCache"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Inherits class BaseCaching for caching system"""

    def put(self, key, item):
        """Load data into cache"""
        if (key or item) is None:
            pass
        self.cache_data[key] = item

    def get(self, key):
        """retrieves values in cache"""
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data[key]
