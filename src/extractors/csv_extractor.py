from .base_extractor import BaseExtractor, timing
from typing import List, Dict, Any, Optional
import csv


class CSVExtractor(BaseExtractor):
    def __init__(self, path: str, delimiter: str = ';'):
        super().__init__(path)
        self.extension = ".csv"
        self.delimiter = delimiter
        self.columns: List[str] = []

    def set_columns(self, columns: Optional[List[str]]):
        self.columns = columns or []

    @timing
    def extract(self) -> List[Dict[str, Any]]:
        with open(self.path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            data = [row for row in reader]
            self.set_columns(reader.fieldnames)
        return data
    
    @timing
    def print_tree(self, data):
        return self.columns
    
    def preview(self, data, n: int = 5):
        return data[:n]
