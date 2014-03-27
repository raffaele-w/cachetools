import unittest

from cachetools import RRCache, rr_cache


@rr_cache(maxsize=2)
def cached(n):
    return n


@rr_cache(maxsize=2, typed=True, lock=None)
def cached_typed(n):
    return n


class RRCacheTest(unittest.TestCase):

    def test_insert(self):
        cache = RRCache(maxsize=2)

        cache['a'] = 1
        cache['b'] = 2
        cache['c'] = 3

        self.assertEqual(len(cache), 2)
        self.assertTrue('a' in cache or ('b' in cache and 'c' in cache))
        self.assertTrue('b' in cache or ('a' in cache and 'c' in cache))
        self.assertTrue('c' in cache or ('a' in cache and 'b' in cache))

    def test_decorator(self):
        self.assertEqual(cached(1), 1)
        self.assertEqual(cached.cache_info(), (0, 1, 2, 1))
        self.assertEqual(cached(1), 1)
        self.assertEqual(cached.cache_info(), (1, 1, 2, 1))
        self.assertEqual(cached(1.0), 1.0)
        self.assertEqual(cached.cache_info(), (2, 1, 2, 1))

    def test_typed_decorator(self):
        self.assertEqual(cached_typed(1), 1)
        self.assertEqual(cached_typed.cache_info(), (0, 1, 2, 1))
        self.assertEqual(cached_typed(1), 1)
        self.assertEqual(cached_typed.cache_info(), (1, 1, 2, 1))
        self.assertEqual(cached_typed(1.0), 1.0)
        self.assertEqual(cached_typed.cache_info(), (1, 2, 2, 2))
        self.assertEqual(cached_typed(1.0), 1.0)
        self.assertEqual(cached_typed.cache_info(), (2, 2, 2, 2))
