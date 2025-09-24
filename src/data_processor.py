from .extractors import BaseExtractor, CSVExtractor, JSONVExtractor, RestAPIExtractor
from typing import Optional, Any


class DataProcessor:
    """
    A class that manages data extraction and delegates operations
    to a given `BaseExtractor` implementation.

    This class acts as a wrapper, allowing you to switch extractors
    dynamically while keeping a consistent interface for working
    with the extracted data.
    """
    def __init__(self, extractor: BaseExtractor):
        self._extractor = extractor
        #self._displayer = displayer   #??? na później

    def set_extractor(self, extractor):
        """Replace the current extractor with a new one."""
        self._extractor = extractor

    def extract_data(self, *args, **kwargs) -> Any:
        """Extract raw data using the current extractor."""
        return self._extractor.extract(*args, **kwargs)
    
    def print_tree_data(self, data: Any, *args, **kwargs):
        """Print or display data in a tree-like structure."""
        return self._extractor.print_tree(data, *args, **kwargs)
    
    def preview_data(self, data: Any, n: int = 5, resource: Optional[str] = None):
        """Preview the first N records/rows/items of the data."""
        if resource is not None:
            return self._extractor.preview(data, n=n, resource=resource)
        return self._extractor.preview(data, n=n)