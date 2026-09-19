from abc import ABC, abstractmethod
from pathlib import Path


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: Path) -> str:
        """Extract text from a document."""
        raise NotImplementedError