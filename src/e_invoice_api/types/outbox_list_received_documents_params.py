# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo
from .document_type import DocumentType

__all__ = ["OutboxListReceivedDocumentsParams"]


class OutboxListReceivedDocumentsParams(TypedDict, total=False):
    date_from: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """Filter by issue date (from)"""

    date_to: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """Filter by issue date (to)"""

    page: int
    """Page number"""

    page_size: int
    """Number of items per page"""

    receiver: Optional[str]
    """
    Filter by receiver (customer_name, customer_email, customer_tax_id,
    customer_company_id, customer_id)
    """

    search: Optional[str]
    """Search in invoice number, seller/buyer names"""

    sender: Optional[str]
    """(Deprecated) Filter by sender ID"""

    sort_by: Literal[
        "created_at", "invoice_date", "due_date", "invoice_total", "customer_name", "vendor_name", "invoice_id"
    ]
    """Field to sort by"""

    sort_order: Literal["asc", "desc"]
    """Sort direction (asc/desc)"""

    type: Optional[DocumentType]
    """Filter by document type. If not provided, returns all types."""
