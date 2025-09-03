from base_extractor import BaseExtractor, timing
import time
import json



class JSONVExtractor(BaseExtractor):
    def __init__(self, path: str): 
        self.extension = ".json"
        #self.config = config
        self.tree = []
        super().__init__(path)

    def set_tree(self, tree):
        self.tree = tree

    @timing
    def extract(self):
        with open(self.path, 'r', encoding='utf-8') as f: 
            return json.load(f) 


    def print_tree(self, data, indent=0):
        tree = []
        branch = " " * indent

        if isinstance(data, dict):
            for key, value in data.items():
                tree.append(f"{branch}{key}")
                tree.extend(self.print_tree(value, indent + 2))
        elif isinstance(data, list):
            tree.append(f"{branch}[]")
            if data:
                tree.extend(self.print_tree(data[0], indent + 2))
        else:
            pass
        return tree
        

    def preview(self, data, n: int = 5):
        return data[:n]