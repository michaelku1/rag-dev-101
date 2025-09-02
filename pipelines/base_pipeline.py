# pipelines/base_pipeline.py
from abc import ABC, abstractmethod

class BasePipeline(ABC):
    @abstractmethod
    def run(self, file_path: str) -> str:
        """Runs the parsing + post-processing pipeline."""
        pass