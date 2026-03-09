# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .document_response import DocumentResponse

__all__ = ["PaginatedDocumentResponse"]


class PaginatedDocumentResponse(BaseModel):
    items: List[DocumentResponse]

    page: int

    page_size: int

    pages: int

    total: int
