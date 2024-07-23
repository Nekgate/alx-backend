#!/usr/bin/env python3
""" Python catching systems. """
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ FIFOcache Class system that inherits from
    Basechaching using LIFO algo to manage cache.
    """

    def __init__(self):
        """ Initialise Class instance. """
        super().__init__()
        self.cache_keys = []

    def put(self, key, item):
        """ Add an item in cache. """
        if key is None or item is None:
            return
        #  Check if cache is full.
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            last_key = self.cache_keys.pop(0)  # Discard the last item (LIFO)
            del self.cache_data[last_key]
            print(f'DISCARD: {last_key}')
        self.cache_keys.append(key)
        self.cache_data[key] = item  # Assign item to key in cache_data.

    def get(self, key):
        """ Get an item by key. """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
