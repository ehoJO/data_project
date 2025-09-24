from abc import ABC, abstractmethod
import time
import pandas as pd

class BaseExtractor(ABC):
    """Base class for all extractors."""
    @abstractmethod
    def extract(self, *args) -> pd.DataFrame:
        pass

    def __init__(self, path):
        self.path = path


def timing(func):
    def wrapper(*args, **kwargs):
        """
        Checking how long does one task take.
        """
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} trwala {end - start:.4f} sekund")
        return result
    return wrapper