from pathlib import Path

from app.services.extractors.base import BaseExtractor
from app.services.extractors.docx import DocxExtractor
from app.services.extractors.pdf import PdfExtractor
from app.services.extractors.txt import TxtExtractor
from app.services.extractors.xlsx import XlsxExtractor


class ExtractionService:
    def __init__(self):
        self.extractors: dict[str, BaseExtractor] = {
            ".txt": TxtExtractor(),
            ".pdf": PdfExtractor(),
            ".docx": DocxExtractor(),
            ".xlsx": XlsxExtractor(),
        }

    def extract(self, file_path: Path) -> str:
        extension = file_path.suffix.lower()

        extractor = self.extractors.get(extension)

        if extractor is None:
            raise ValueError(
                f"Unsupported file type: {extension or 'unknown'}"
            )

        return extractor.extract(file_path)


extraction_service = ExtractionService()