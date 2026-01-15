# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo
from .document_type import DocumentType
from .document_state import DocumentState

__all__ = ["InboxListParams"]


class InboxListParams(TypedDict, total=False):
    date_from: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """Filter by issue date (from)"""

    date_to: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """Filter by issue date (to)"""

    page: int
    """Page number"""

    page_size: int
    """Number of items per page"""

    search: Optional[str]
    """Search in invoice number, seller/buyer names"""

    sender: Optional[str]
    """Filter by sender (vendor_name, vendor_email, vendor_tax_id, vendor_company_id)"""

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
