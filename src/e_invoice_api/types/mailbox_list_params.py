from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["MailboxListParams"]


class MailboxListParams(TypedDict, total=False):
    page: int
    """Page number"""

    page_size: int
    """Number of items per page"""

    processed: Optional[bool]
    """Filter by processing status.

    If not provided, returns all. Ignored when `status` is set.
    """

    received_from: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """
    Inclusive lower bound on received date (falls back to created_at when
    received_at is null)
    """

    received_to: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """
    Inclusive upper bound on received date (falls back to created_at when
    received_at is null)
    """

    search: Optional[str]
    """
    Case-insensitive search across sender email, subject, message ID, and attachment
    filenames
    """

    sort_by: Literal["received_at", "created_at"]
    """Field to sort by"""

    sort_order: Literal["asc", "desc"]
    """Sort direction (asc/desc)"""

    status: Optional[Literal["pending", "success", "failed"]]
    """Filter by status: pending, success, or failed.

    Takes precedence over `processed` if both are provided.
    """
