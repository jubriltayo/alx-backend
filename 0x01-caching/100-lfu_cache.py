#!/usr/bin/env python3
""" Defines LFUCache """
from base_caching import BaseCaching
from collections import OrderedDict


class LFUCache(BaseCaching):
    """ An LFU caching system """
    def __init__(self):
        """ Initializes the cache """
        super().__init__()
        self.cache_data = OrderedDict()
        self.keys_frequency = []

    def put(self, key, item):
        """ Adds an item to the cache """

        # Check if key or item is None, and return early if so
        if key is None or item is None:
            return

        # Check if the key is not already in the cache
        if key not in self.cache_data:
            # Check if adding the new item would exceed the cache size
            if len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
                # If the cache is full, remove the least frequently
                # used item (LFU)
                lfu_key, _ = self.keys_frequency[-1]
                self.cache_data.pop(lfu_key)
                self.keys_frequency.pop()
                print("DISCARD:", lfu_key)

            # Add the new key-value pair to the cache
            self.cache_data[key] = item

            # Find the position to insert the new key-frequency pair in
            # the keys_frequency list
            insert_index = len(self.keys_frequency)
            for i, key_freq in enumerate(self.keys_frequency):
                # Check if the frequency of the current key is 0 (newly added)
                if key_freq[1] == 0:
                    insert_index = i
                    break

            # Insert the new key-frequency pair into the keys_frequency list
            self.keys_frequency.insert(insert_index, [key, 0])
        else:
            # If the key is already in the cache, update its value
            self.cache_data[key] = item

            # Reorder the keys in the keys_frequency list based on
            # frequency after updating the key's frequency
            self.__reorder_items(key)

    def get(self, key):
        """Retrieves data from the cache """
        if key is not None and key in self.cache_data:
            # Since the key is accessed, reorder the keys in
            # keys_frequency based on frequency
            self.__reorder_items(key)

        # Return the value associated with the given key from the cache
        # If the key does not exist in the cache, return None
        return self.cache_data.get(key, None)

    def __reorder_items(self, mru_key):
        """ reorders items in the cache based on usage (MRU) """
        # List to store the positions of keys with the maximum frequency
        max_positions = []
        mru_frequency = 0  # Frequency of the most recently used key

        # Position of the most recently used key in keys_frequency
        mru_position = 0

        # Position to insert the most recently used key back in
        # keys_frequency
        position_inserted = 0

        # Loop through the keys_frequency list to find the most
        # recently used key and keys with maximum frequency
        for i, key_freq in enumerate(self.keys_frequency):
            if key_freq[0] == mru_key:
                # Increment the frequency of the most recently used key
                mru_frequency = key_freq[1] + 1

                # Save the position of the most recently used key
                mru_position = i
                break
            elif len(max_positions) == 0:
                max_positions.append(i)
            elif key_freq[1] < self.keys_frequency[max_positions[-1]][1]:
                max_positions.append(i)

        # Reverse the list of positions to get them in ascending
        # order of frequency
        max_positions.reverse()

        # Find the position to insert the most recently used key
        # back in keys_frequency
        for pos in max_positions:
            if self.keys_frequency[pos][1] > mru_frequency:
                break
            position_inserted = pos

        # Remove the most recently used key from keys_frequency and
        # reinsert it at the correct position based on frequency
        self.keys_frequency.pop(mru_position)
        self.keys_frequency.insert(position_inserted, [mru_key, mru_frequency])
