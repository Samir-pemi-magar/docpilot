import asyncio

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.models import Document
from app.services.processing import document_processing_service
from app.services.storage import storage_service


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


@router.post("/")
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    document = Document(
        filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        size=size,
        status="uploading",
        storage_key="",
    )

    db.add(document)
    await db.flush()

    document.storage_key = f"{document.id}/original"

    try:
        await asyncio.to_thread(
            storage_service.upload_file,
            file.file,
            document.storage_key,
            document.content_type,
        )
    except Exception:
        document.status = "failed"
        await db.commit()
        raise

    document.status = "uploaded"

    try:
        await db.commit()
    except Exception:
        await db.rollback()

        try:
            await asyncio.to_thread(
                storage_service.delete_file,
                document.storage_key,
            )
        except Exception:
            pass

        raise

    extracted_storage_key: str | None = None

    try:
        document.status = "processing"
        await db.commit()

        _, extracted_storage_key = await (
            document_processing_service.process_document(document)
        )

        document.extracted_storage_key = extracted_storage_key
        document.status = "extracted"

        await db.commit()

    except Exception:
        await db.rollback()

        document.status = "failed"
        await db.commit()

        if extracted_storage_key is not None:
            try:
                await asyncio.to_thread(
                    storage_service.delete_file,
                    extracted_storage_key,
                )
            except Exception:
                pass

        raise

    return {
        "id": document.id,
        "filename": document.filename,
        "content_type": document.content_type,
        "status": document.status,
        "storage_key": document.storage_key,
        "extracted_storage_key": document.extracted_storage_key,
    }
