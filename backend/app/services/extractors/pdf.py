from pathlib import Path

import pymupdf

from app.services.extractors.base import BaseExtractor


class PdfExtractor(BaseExtractor):
    def extract(self, file_path: Path) -> str:
        document = pymupdf.open(file_path)

        try:
            pages = [
                page.get_text()
                for page in document
            ]

            return "\n".join(pages)
        finally:
            document.close()