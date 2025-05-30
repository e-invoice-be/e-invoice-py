# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["DocumentAttachment"]


class DocumentAttachment(BaseModel):
    id: str

    file_name: str

    file_size: Optional[int] = None

    file_type: Optional[str] = None

    file_url: Optional[str] = None
