#!/usr/bin/env python3
"""This module defines class LFUCache"""
from base_caching import BaseCaching
from collections import OrderedDict


class LFUCache(BaseCaching):
    """An LFU caching system"""
    def __init__(self):
        """Initializes the cache"""
        super().__init__()
        self.cache_data = OrderedDict()
        self.keys_frequency = []

    def put(self, key, item):
        """load data into cache"""
        if key and item:
            if key not in self.cache_data:
                if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                    lfu_key, _ = self.keys_frequency[-1]
                    self.cache_data.pop(lfu_key)
                    self.keys_frequency.pop()
                    print(f"DISCARD: {lfu_key}")

                self.cache_data[key] = item

                # locate position to insert new key-frequency pair in list
                insert_index = len(self.keys_frequency)
                for i, key_freq in enumerate(self.keys_frequency):
                    # check if frequency of current key is 0 implying new key
                    if key_freq[1] == 0:
                        insert_index = i
                        break

                # insert new key-frequency pair into list
                self.keys_frequency.insert(insert_index, [key, 0])

            else:
                self.cache_data[key] = item

                # reorder keys in list based on frequency after
                # updating key's frequency
                self.__reorder_items(key)

    def get(self, key):
        """retrieve item in cache"""
        if key and key in self.cache_data:
            self.__reorder_items(key)
        return self.cache_data.get(key, None)

    def __reorder_items(self, mru_key):
        """reorders items in cache based on usage (MRU)"""
        # list to store position of keys with max frequency
        max_positions = []
        mru_frequency = 0
        mru_position = 0
        position_inserted = 0

        for i, key_freq in enumerate(self.keys_frequency):
            if key_freq[0] == mru_key:
                mru_frequency = key_freq[1] + 1

                # save position of most recently used key
                mru_position = 1
                break
            elif len(max_positions) == 0:
                max_positions.append(i)
            elif key_freq[1] < self.keys_frequency[max_positions[-1]][1]:
                max_positions.append(i)

        # reverse list of positions to ascend them in order of frequency
        max_positions.reverse()

        # locate position to insert the mru key back in key frequency
        for pos in max_positions:
            if self.keys_frequency[pos][1] > mru_frequency:
                break
            position_inserted = pos

        # remove mru key from keys_frequency and
        # reinsert it at the coorect position based on frequency
        self.keys_frequency.pop(mru_position)
        self.keys_frequency.insert(position_inserted, [mru_key, mru_frequency])
