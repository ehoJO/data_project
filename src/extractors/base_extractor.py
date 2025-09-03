import time

class BaseExtractor:
    """Base class for all extractors."""
    def __init__(self, path):
        self.path = path


def timing(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} trwala {end - start:.4f} sekund")
        return result
    return wrapper