from src.extractors import CSVExtractor, JSONVExtractor, RestAPIExtractor
from src.transformers import DictColumnTransformer, NullCheckerTransformer, PipelineTransfomer
from src.data_processor import DataProcessor
import requests
import json
import pandas as pd


if __name__ == "__main__":
    fetcher = RestAPIExtractor(api_key="9369a5ad92b5bf33193a720693c63ed7", base_url = "https://api.themoviedb.org/3")
    df =  fetcher.extract("/movie/popular", "results", [], 'id', ["title", "release_date", "overview", "vote_average"], True, pages=2)
    df_ids = [str(id) for id in df['id'].unique()]

    reviews = fetcher.extract("/movie", "results", [], "id", ['author', 'content', 'author_details'], True, ids_list = df_ids, path_second = "/reviews")
    #cast = fetcher.extract("/movie", "cast", [], "id", ['name', 'character', 'order'], True, ids_list = df_ids, path_second = "/credits")
    
    pipelineTransformer = PipelineTransfomer([DictColumnTransformer('author_details', False), NullCheckerTransformer()])

    reviews_cleaned = pipelineTransformer.transform(reviews)
    print(reviews_cleaned.head())