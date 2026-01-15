# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

from .document_type import DocumentType
from .document_state import DocumentState

__all__ = ["OutboxListDraftDocumentsParams"]


class OutboxListDraftDocumentsParams(TypedDict, total=False):
    page: int
    """Page number"""

    page_size: int
    """Number of items per page"""

    search: Optional[str]
    """Search in invoice number, seller/buyer names"""

    sort_by: Literal[
        "created_at", "invoice_date", "due_date", "invoice_total", "customer_name", "vendor_name", "invoice_id"
    ]
    """Field to sort by"""

    sort_order: Literal["asc", "desc"]
    """Sort direction (asc/desc)"""

    state: Optional[DocumentState]
    """Filter by document state"""

    type: Optional[DocumentType]
    """Filter by document type"""
