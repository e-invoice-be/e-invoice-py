# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .._types import FileTypes

__all__ = ["DocumentCreateFromPdfParams"]


class DocumentCreateFromPdfParams(TypedDict, total=False):
    file: Required[FileTypes]

    customer_tax_id: Optional[str]

    vendor_tax_id: Optional[str]
