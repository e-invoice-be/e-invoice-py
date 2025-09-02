# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["DocumentAttachmentCreateParam"]


class DocumentAttachmentCreateParam(TypedDict, total=False):
    file_name: Required[str]

    file_data: Optional[str]
    """Base64 encoded file data"""

    file_size: int

    file_type: str
