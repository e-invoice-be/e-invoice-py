# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo
from .document_type import DocumentType
from .document_state import DocumentState

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

    search: Optional[str]
    """Search in invoice number, seller/buyer names"""

    sender: Optional[str]
    """Filter by sender ID"""

    state: Optional[DocumentState]
    """Filter by document state"""

    type: Optional[DocumentType]
    """Filter by document type"""
