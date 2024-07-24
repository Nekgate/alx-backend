#!/usr/bin/env python3
""" Python catching systems. """
from base_caching import BaseCaching
from collections import OrderedDict


class LFUCache(BaseCaching):
    """ LFUCache class.
    that implements a Least Frequently Used (LFU) caching system
    """

    def __init__(self):
        """ Initialise the LFUCache. """
        super().__init__()
        self.frequency = {}  # Tracks the frequency of each key
        self.usage = {}  # Tracks the usage order for each frequency level
        self.current_usage = 0  # Tracks the global usage order

    def put(self, key, item):
        """ Add an item in cache.
        If key or item is None, this method should not do anything.
        If the number of items in self.cache_data
        is higher than BaseCaching.MAX_ITEMS,
        discard the least frequency used item (LFU algorithm).
        If there are multiple items with the same frequency,
        discard the least recently used one (LRU).
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self._update_frequency(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                self._evict()
            self.cache_data[key] = item
            self.frequency[key] = 1
            if 1 not in self.usage:
                self.usage[1] = {}
            self.current_usage += 1
            self.usage[1][key] = self.current_usage

    def get(self, key):
        """
        Get an item by key.

        Must return the value in self.cache_data linked to key.
        If key is None or if the key doesn’t
        exist in self.cache_data, return None.
        """
        if key is None or key not in self.cache_data:
            return None
        # Update the frequency and return the item
        self._update_frequency(key)
        return self.cache_data[key]

    def _update_frequency(self, key):
        """
        Update the frequency and usage order of a key.

        This method is used internally to maintain the correct LFU order.
        """
        freq = self.frequency[key]
        del self.usage[freq][key]
        if not self.usage[freq]:
            del self.usage[freq]
        self.frequency[key] += 1
        freq += 1
        if freq not in self.usage:
            self.usage[freq] = {}
        self.current_usage += 1
        self.usage[freq][key] = self.current_usage

    def _evict(self):
        """ Evict the least frequently used item from the cache.

        If there are multiple items with the same frequency,
        evict the least recently used one.
        This method is used internally to
        ensure the cache size does not exceed MAX_ITEMS.
        """
        min_freq = min(self.usage)
        least_used = min(self.usage[min_freq], key=self.usage[min_freq].get)
        del self.cache_data[least_used]
        del self.frequency[least_used]
        del self.usage[min_freq][least_used]
        if not self.usage[min_freq]:
            del self.usage[min_freq]
        print(f"DISCARD: {least_used}")
