from pathlib import Path

from docx import Document

from app.services.extractors.base import BaseExtractor


class DocxExtractor(BaseExtractor):
    def extract(self, file_path: Path) -> str:
        document = Document(file_path)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
        ]

        return "\n".join(paragraphs)