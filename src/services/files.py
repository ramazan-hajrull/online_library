import uuid

from fastapi import UploadFile, HTTPException, status
from pathlib import Path


UPLOAD_DIR = Path("uploads")
ALLOWED_COVER_EXT = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_BOOK_EXT = {".pdf", ".epub"}
MAX_UPLOAD_MB = 25


def _save_upload(file: UploadFile, subdir: str, allowed_ext: set[str]) -> str:
    ext = Path(file.filename or "").suffix.lower()
    if ext not in allowed_ext:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Недопустимый тип файла. Разрешены: {', '.join(sorted(allowed_ext))}",
        )

    target_dir = UPLOAD_DIR / subdir
    target_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{ext}"
    destination = target_dir / filename

    max_bytes = MAX_UPLOAD_MB * 1024 * 1024
    size = 0
    with destination.open("wb") as out:
        while chunk := file.file.read(1024 * 1024):
            size += len(chunk)
            if size > max_bytes:
                destination.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"Файл превышает лимит {MAX_UPLOAD_MB}",
                )
            out.write(chunk)

    return str(destination)


def save_cover(file: UploadFile) -> str:
    return _save_upload(file, "covers", ALLOWED_COVER_EXT)


def save_book_file(file: UploadFile) -> str:
    return _save_upload(file, "books", ALLOWED_BOOK_EXT)


def delete_file(path: str | None) -> None:
    if path:
        Path(path).unlink(missing_ok=True)