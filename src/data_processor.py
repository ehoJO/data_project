from extractors import BaseExtractor, CSVExtractor, JSONVExtractor


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
        #self._displayer = displayer   #??? jst potrzeba tych wszystkich funkcji? czy już  samym extraktorze mogę mieć 

    def set_extractor(self, extractor):
        """Replace the current extractor with a new one."""
        self._extractor = extractor

    def extract_data(self):
        """Extract raw data using the current extractor."""
        return self._extractor.extract()
    
    def print_tree_data(self, data):
        """Print or display data in a tree-like structure."""
        return self._extractor.print_tree(data)

    def preview_data(self, data, n):
        """Preview the first N records/rows/items of the data."""
        return self._extractor.preview(data, n)


if __name__ == "__main__":
    csv_path = "first_tasks/task3_data/ecommerce_clickstream_transactions.csv"
    json_path = "first_tasks/weather.json"

    csv_extractor = CSVExtractor(csv_path, ';')
    json_extractor = JSONVExtractor(json_path)

    # czym jest kontekst a strategia? bo chyba rozumiałam i już nie rozumiem xd

    processor = DataProcessor(csv_extractor)
    data = processor.extract_data()
    print(processor.print_tree_data(data))

    processor.set_extractor(json_extractor)
    data2 = processor.extract_data()#processor.print_tree_data()
    print("\n".join(processor.print_tree_data(data2)))


    print(data2)