from functools import lru_cache

from app.services.processor import DocumentProcessor


@lru_cache
def get_processor() -> DocumentProcessor:
    return DocumentProcessor()
