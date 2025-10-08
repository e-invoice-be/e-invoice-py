# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["DocumentAttachmentCreate"]


class DocumentAttachmentCreate(BaseModel):
    file_name: str

    file_data: Optional[str] = None
    """Base64 encoded file data"""

    file_size: Optional[int] = None

    file_type: Optional[str] = None
