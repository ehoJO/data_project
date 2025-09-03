from extractors import BaseExtractor, CSVExtractor, JSONVExtractor


class DataProcessor:

    def __init__(self, extractor: BaseExtractor):
        self._extractor = extractor
        #self._displayer = displayer   #??? jst potrzeba tych wszystkich funkcji? czy już  samym extraktorze mogę mieć 

    def set_extractor(self, extractor):
        self._extractor = extractor

    def extract_data(self):
        return self._extractor.extract()
    
    def print_tree_data(self, data):
        return self._extractor.print_tree(data)

    def preview_data(self, data, n):
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