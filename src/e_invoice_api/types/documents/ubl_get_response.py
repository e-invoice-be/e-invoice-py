# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["UblGetResponse"]


class UblGetResponse(BaseModel):
    id: str

    file_name: str

    file_hash: Optional[str] = None

    file_size: Optional[int] = None

    receiver_peppol_id: Optional[str] = None

    receiver_peppol_scheme: Optional[str] = None

    sender_peppol_id: Optional[str] = None

    sender_peppol_scheme: Optional[str] = None

    signed_url: Optional[str] = None

    validated_at: Optional[datetime] = None
