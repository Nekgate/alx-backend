#!/usr/bin/env python3
""" Python catching systems. """
from base_caching import BaseCaching
from collections import OrderedDict


class LRUCache(BaseCaching):
    """ LRU Class caching system.
    Use of OrderedDict which keep order of insertion of keys
    The order shows how recently they were used.
    In the beginning is the least recently used and in the end,
    the most recently used.
    Any update OR query made to a key moves to the end (most recently used).
    If anything is added, it is added at the end (most recently used/added).
    All operations have O(1) time complexity.
    """

    def __init__(self):
        """ Initialise Class instance. """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """ Add an item in cache.
        First, add/ update the key by conventional methods.
        And also move the key to the end to show that it was recently used.
        But here we will also check if the length of our dictionary
        has exceeded our capacity.
        If so remove the first key (least recently used)
        """
        if key is not None and item is not None:
            self.cache_data[key] = item
            self.cache_data.move_to_end(key)
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                discarded = self.cache_data.popitem(last=False)
                print('DISCARD: {}'.format(discarded[0]))

    def get(self, key):
        """ Get an item by key.
        return the value of the key that is required in O(1) and return -1 if the
        key is not found, also move key to end as evidence it was recently used.
        """
        if key is not None and key in self.cache_data:
            self.cache_data.move_to_end(key)
        return self.cache_data.get(key)