"""
Parallel - Multiprocessing and caching utilities for performance.
Uses ThreadPoolExecutor for concurrent forecasting tasks.
"""

import functools
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


_CACHE = {}
_CACHE_TIMES = {}
CACHE_TTL = 300


def cached(key, ttl=CACHE_TTL):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{key}_{str(args)}_{str(kwargs)}"
            now = time.time()
            if cache_key in _CACHE:
                if now - _CACHE_TIMES.get(cache_key, 0) < ttl:
                    return _CACHE[cache_key]
            result = func(*args, **kwargs)
            _CACHE[cache_key] = result
            _CACHE_TIMES[cache_key] = now
            return result
        return wrapper
    return decorator


def clear_cache():
    _CACHE.clear()
    _CACHE_TIMES.clear()


def run_parallel(tasks, max_workers=4):
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_key = {executor.submit(func): key for key, func in tasks.items()}
        for future in as_completed(future_to_key):
            key = future_to_key[future]
            try:
                results[key] = future.result()
            except Exception as e:
                results[key] = {"error": str(e)}
    return results