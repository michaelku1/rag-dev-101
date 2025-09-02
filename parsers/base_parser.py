from abc import ABC, abstractmethod
import pandas as pd

class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: str):
        """
        parse method wrapper, handling data objects conversion (e.g pd.dataframe)
        and data structure (e.g file and sheets)
        """

        pass

    def _parse_data(self, df: pd.DataFrame, **kwargs):
        """
        main parsing method logic, tools
        """

        pass






