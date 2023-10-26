#!/usr/bin/python3
""" Defines FIFOCache """
from base_caching import BaseCaching
from collections import OrderedDict


class LRUCache(BaseCaching):
    """ A FIFO caching system """
    def __init__(self):
        """ Initializes our cache """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """ Inserts values to cache """
        if key is None or item is None:
            return
        if key not in self.cache_data:
            if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                lru_key, _ = self.cache_data.popitem(True)
                print("DISCARD:", lru_key)
            self.cache_data[key] = item
            self.cache_data.move_to_end(key, last=False)
        else:
            self.cache_data[key] = item

    def get(self, key):
        """ Retrives data from our cache """
        if key is not None and key in self.cache_data:
            self.cache_data.move_to_end(key, last=False)
        return self.cache_data.get(key, None)
