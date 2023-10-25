#!/usr/bin/env python3
"""This module defines class BasicCache"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Inherits class BaseCaching for caching system"""

    def __init__(self):
        """Initializes the class attributes"""
        super().__init__()

    def put(self, key, item):
        """Load data into cache"""
        if (key or item) is None:
            pass
        self.cache_data[key] = item

    def get(self, key):
        """retrieves values in cache"""
        return self.cache_data.get(key, None)
