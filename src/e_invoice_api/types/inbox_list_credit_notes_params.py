# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["InboxListCreditNotesParams"]


class InboxListCreditNotesParams(TypedDict, total=False):
    page: int
    """Page number"""

    page_size: int
    """Number of items per page"""
