from base_extractor import BaseExtractor, timing
import csv


class CSVExtractor(BaseExtractor):
    def __init__(self, path: str, delimiter: str):
        self.extension = ".csv"
        self.delimiter = delimiter
        self.columns = []
        super().__init__(path)

    def set_columns(self, columns):
        self.columns = columns

    @timing
    def extract(self):
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
