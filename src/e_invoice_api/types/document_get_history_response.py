# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["DocumentGetHistoryResponse", "DocumentGetHistoryResponseItem"]


class DocumentGetHistoryResponseItem(BaseModel):
    action: str

    created_at: datetime

    success: bool

    updated_at: datetime

    error_message: Optional[str] = None


DocumentGetHistoryResponse: TypeAlias = List[DocumentGetHistoryResponseItem]
