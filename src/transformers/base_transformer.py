import time
from abc import ABC, abstractmethod
import pandas as pd

class BaseTransformer(ABC):
    """Base class for all extractors."""
    @abstractmethod
    def transform(self) -> pd.DataFrame:
        pass


class PipelineTransfomer(BaseTransformer):
    def __init__(self,
                 transformers):
        self.transformers = list(transformers)

    def transform(self,
                  df = pd.DataFrame) -> pd.DataFrame:
        current_df = df
        for transformation in self.transformers:
            current_df = transformation.transform(current_df)
        
        return current_df
    
