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

    def put(self, key, item):
        """ Add an item in cache. """
        if key and item:
            self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            self.cache_data.pop(self.last_item)
            print(f'DISCARD: {self.last_item}')
        if key:
            self.last_item = key

    def get(self, key):
        """ Get an item by key. """
        return self.cache_data.get(key)
