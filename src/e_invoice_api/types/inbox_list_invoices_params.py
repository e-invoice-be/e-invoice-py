# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["InboxListInvoicesParams"]


class InboxListInvoicesParams(TypedDict, total=False):
    page: int
    """Page number"""

    page_size: int
    """Number of items per page"""

    sort_by: Literal[
        "created_at", "invoice_date", "due_date", "invoice_total", "customer_name", "vendor_name", "invoice_id"
    ]
    """Field to sort by"""

    sort_order: Literal["asc", "desc"]
    """Sort direction (asc/desc)"""
