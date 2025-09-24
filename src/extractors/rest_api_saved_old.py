from src.extractors.base_extractor import BaseExtractor, timing
from typing import Any, Dict, List, Optional
import sys
import os
import json
import requests
import pandas as pd



class RestAPIExtractor(BaseExtractor):
    def __init__(self, api_key: str, base_url: str, path: Optional[str] = None, session: Optional[requests.Session] = None): 
        super().__init__(path)
        self.api_key = api_key
        self.base_url = base_url
        self.session = session or requests.Session()

    def _get(self, endpoint: str, params: dict | None = None, headers = None) -> dict:
        if params is None: 
            params = {}
        params["api_key"] = self.api_key
        response = self.session.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    
    def extract(self, path, pages, result_key, deafult_empty_result, identifier_column, columns, with_identifier):
        # path = "/movie/popular"
        # pages = 2
        # result_key = "results"
        # deafult_empty_result = []
        # identifier_column = "id"
        # columns = ["title", "release_date", "overview", "vote_average"]
        # with_identifier = True  

        entities = self.get_entities(path, result_key, deafult_empty_result, pages)
        return self.collect_entities_dataframe(entities, columns, identifier_column, with_identifier)

    def get_entities(self, path: str, result_key: str, deafult_empty_result, pages: int = 1) -> List[Dict]: # pages jest nieobowiązkowe -> ify
        entities = []
        for page in range(1, pages + 1):
            data = self._get(path, {"page": page})
            entities.extend(data.get(result_key, deafult_empty_result))
        return entities

    def get_entity_ids(self, entities: list[dict], identifier_column: str) -> list[str]:
        return [entity[identifier_column] for entity in entities]
    
    def collect_entities_dataframe(self, entities: List[Dict], columns, identifier_column, with_identifier) -> pd.DataFrame:
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


class MoviesAPI(RestAPIExtractor):
    def __init__(self, path, pages, result_key, default_empty_result, identifier_column, columns, with_identifier):
        self.path = "/movie/popular"
        pages = 2
        result_key = "results"
        deafult_empty_result = []
        identifier_column = "id"
        columns = ["title", "release_date", "overview", "vote_average"]
        with_identifier = True


    def get_popular_movies(self, pages: int = 1) -> List[Dict]:
        movies = []
        for page in range(1, pages + 1):
            data = self._get("/movie/popular", {"page": page})
            movies.extend(data.get("results", []))
        return movies

# połączyć te cztery funkcje w jedna uniwersalna
    def get_movie_details(self, movie_id: int) -> Dict:
        return self._get(f"/movie/{movie_id}")

    def get_movie_reviews(self, movie_id: int) -> List[Dict]:
        data = self._get(f"/movie/{movie_id}/reviews")
        return data.get("results", [])

    def get_movie_cast(self, movie_id: int) -> List[Dict]:
        data = self._get(f"/movie/{movie_id}/credits")
        return data.get("cast", [])


# połączyć wszystie 3 collecty w jedno
    def collect_movies_dataframe(self, movies: List[Dict]) -> pd.DataFrame:
        rows = []
        for movie in movies:
            try:
                #details = self.get_movie_details(movie["id"])
                #genres = ", ".join([g["name"] for g in details.get("genres", [])])
                rows.append({
                    "id": movie["id"],
                    "title": movie.get("title"),
                    "release_date": movie.get("release_date"),
                   # "genres": genres,
                    "overview": movie.get("overview"),
                    "vote_average": movie.get("vote_average")
                })
            except Exception as e:
                print(f"Warning: błąd podczas pobierania szczegółów filmu {movie.get('id')}: {e}")
        return pd.DataFrame(rows)

    def collect_reviews_dataframe(self, movie_ids: List[int]) -> pd.DataFrame:
        rows = []
        for movie_id in movie_ids:
            try:
                for r in self.get_movie_reviews(movie_id):
                    rows.append({
                        "movie_id": movie_id,
                        "author": r.get("author"),
                        "content": r.get("content"),
                        "rating": r.get("author_details", {}).get("rating")
                    })
            except Exception as e:
                print(f"Warning: błąd podczas pobierania recenzji {movie_id}: {e}")
        return pd.DataFrame(rows)

    def collect_cast_dataframe(self, movie_ids: List[int], top_n: int = 5) -> pd.DataFrame:
        rows = []
        for movie_id in movie_ids:
            try:
                for c in self.get_movie_cast(movie_id)[:top_n]:
                    rows.append({
                        "movie_id": movie_id,
                        "actor_name": c.get("name"),
                        "character": c.get("character"),
                        "order": c.get("order")
                    })
            except Exception as e:
                print(f"Warning: błąd podczas pobierania obsady {movie_id}: {e}")
        return pd.DataFrame(rows)

    @timing
    def extract(self, pages: int = 1) -> Dict[str, List[Dict]]:
        movies = self.get_popular_movies(pages)
        movie_ids = [m["id"] for m in movies]
        movies_df = self.collect_movies_dataframe(movies)
        reviews_df = self.collect_reviews_dataframe(movie_ids)
        cast_df = self.collect_cast_dataframe(movie_ids)
        return {
            "movies": movies_df.to_dict(orient="records"),
            "reviews": reviews_df.to_dict(orient="records"),
            "cast": cast_df.to_dict(orient="records")
        }

    def preview(self, data: Any, n: int = 5, resource: Optional[str] = None) -> Any:
        if isinstance(data, dict):
            if resource:
                return data.get(resource, [])[:n]
            return {k: v[:n] if isinstance(v, list) else v for k, v in data.items()}
        if isinstance(data, list):
            return data[:n]
        return data
    
    #def print_tree(self, )


if __name__ == '__main__':

    api_key = "9369a5ad92b5bf33193a720693c63ed7"
    base_url = "https://api.themoviedb.org/3"

    movie_extractor = RestAPIExtractor(api_key, base_url)   
    df = movie_extractor.extract("/movie/popular", 2, "results", [], 'id', ["title", "release_date", "overview", "vote_average"], False)
    print(df.head(5))

    # path = "/movie/popular"
        # pages = 2
        # result_key = "results"
        # deafult_empty_result = []
        # identifier_column = "id"
        # columns = ["title", "release_date", "overview", "vote_average"]
        # with_identifier = True  

        # "movie_id": movie_id,
        #                 "author": r.get("author"),
        #                 "content": r.get("content"),
        #                 "rating": r.get