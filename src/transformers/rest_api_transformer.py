from src.transformers.base_transformer import BaseTransformer
import pandas as pd

class DictColumnTransformer(BaseTransformer):
    def __init__(self,
                 column: str,
                 drop_original: bool = True):
        self.column = column
        self.drop_original = drop_original

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        column_info = df[self.column]

        normalized = pd.json_normalize(column_info)
        normalized.index = df.index
        df = df.join(normalized)

        if self.drop_original:
            df = df.drop(columns=[self.column])

        return df
    



class NullCheckerTransformer(BaseTransformer):
    def __init__(self):
        self.null_report: dict[str, int] = {}

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.null_report = df.isnull().sum()
        print(f"Znaleziono null'e w kolumnach: {self.null_report}")
        return df
    