from abc import ABC, abstractmethod
import pandas as pd

class DatabaseInterface(ABC):
    @abstractmethod
    def get_data(self, query: str) -> pd.DataFrame:
        pass