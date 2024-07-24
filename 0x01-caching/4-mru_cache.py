#!/usr/bin/env python3
""" Python catching systems. """
from base_caching import BaseCaching
from collections import OrderedDict


class MRUCache(BaseCaching):
    """ MRU Class caching system.
    """
    def __init__(self):
        """ Initialise Class instance. """
        super().__init__()
        self.cache_data = OrderedDict()
        self.mru = ""

    def put(self, key, item):
        """ Add an item in cache.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            del self.cache_data[key]

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            if self.mru is not None:
                del self.cache_data[self.mru]
                print("DISCARD: {}".format(self.mru))

        self.cache_data[key] = item
        self.mru = key

    def get(self, key):
        """ Get an item by key.
        """
        if key is None or key not in self.cache_data:
            return None

        self.mru = key
        return self.cache_data[key]
