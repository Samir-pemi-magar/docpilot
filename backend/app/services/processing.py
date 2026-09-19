import asyncio
import tempfile
from pathlib import Path

from app.models import Document
from app.services.cleaning import text_cleaning_service
from app.services.extraction import extraction_service
from app.services.storage import storage_service


class DocumentProcessingService:
    async def extract_document(self, document: Document) -> str:
        suffix = Path(document.filename).suffix.lower()
        temporary_path: Path | None = None

        try:
            with tempfile.NamedTemporaryFile(
                suffix=suffix,
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)

            with temporary_path.open("wb") as file_object:
                await asyncio.to_thread(
                    storage_service.download_file,
                    document.storage_key,
                    file_object,
                )

            return await asyncio.to_thread(
                extraction_service.extract,
                temporary_path,
            )
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)

    async def process_document(
        self,
        document: Document,
    ) -> tuple[str, str]:
        extracted_text = await self.extract_document(document)

        cleaned_text = await asyncio.to_thread(
            text_cleaning_service.clean,
            extracted_text,
        )

        extracted_storage_key = f"{document.id}/extracted.txt"

        await asyncio.to_thread(
            storage_service.upload_text,
            cleaned_text,
            extracted_storage_key,
        )

        return cleaned_text, extracted_storage_key


document_processing_service = DocumentProcessingService()
