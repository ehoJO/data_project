from src.extractors.base_extractor import BaseExtractor, timing
from typing import Any, Dict, List, Optional
import sys
import os
import json
import requests
import pandas as pd



class RestAPIExtractor(BaseExtractor):
    def __init__(self, api_key: str, 
                 base_url: str, 
                 session: requests.Session | None = None): 
        #super().__init__(path)
        self.api_key = api_key
        self.base_url = base_url
        self.session = session or requests.Session()

    def _get(self, 
             endpoint, 
             params=None):
        
        if params is None:
            params = {}
        params["api_key"] = self.api_key
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    

    def extract(self, 
                path_first, 
                result_key, 
                default_empty_result, 
                identifier_column, 
                columns, 
                with_identifier, 
                ids_list: list | None = None, 
                path_second: str | None = None, 
                pages: int | None = None):

        entities = self.get_entities(path_first, result_key, default_empty_result, pages, ids_list, path_second)
        return self.collect_entities_dataframe(entities, columns, identifier_column, with_identifier)
    

    def get_entities(self, 
                     path_first: str, 
                     result_key: str, 
                     default_empty_result, 
                     pages: int | None = None, 
                     ids_list: list | None = None, 
                     path_second: str | None = None) -> list[dict]:
        
        entities = []
        page_range = range(1, pages + 1) if pages else [None]

        paths = ([path_first + '/' + id_ + path_second for id_ in ids_list] if ids_list else [path_first])

        for page in page_range:
            params = {"page": page} if page else None
            for path in paths:
                data = self._get(path, params)
                entities.extend(data.get(result_key, default_empty_result))
        
        return entities
        

    def collect_entities_dataframe(self, 
                                   entities: list[dict], 
                                   columns, 
                                   identifier_column, 
                                   with_identifier) -> pd.DataFrame:
    
        rows = []
        for entity in entities:
            try:
                row = {column: entity[column] for column in columns}
                if with_identifier:
                    row[identifier_column] = entity[identifier_column]
                rows.append(row)
            except Exception as e:
                print(f"Warning: błąd podczas pobierania szczegółów filmu {entity.get(identifier_column)}: {e}")
        return pd.DataFrame(rows)