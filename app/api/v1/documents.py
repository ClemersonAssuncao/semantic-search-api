from typing import List
from fastapi import APIRouter

from app.schemas.document import DocumentRead, DocumentCreate

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])

@router.post("/", response_model=List[DocumentRead])
def create_document(
    payload: List[DocumentCreate],
):
    docs = []
    for i, doc in enumerate(payload):
        print(f"Creating document: {doc.title}")
        docs.append(DocumentRead(
            id=i + 1,
            title=doc.title,
            content=doc.content,
        ))

    return docs