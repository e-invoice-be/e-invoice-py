from typing import List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["InboundEmail", "Attachment"]


class Attachment(BaseModel):
    filename: str

    content_type: Optional[str] = None

    size: Optional[int] = None


class InboundEmail(BaseModel):
    id: str

    created_at: datetime

    message_id: str

    sender_email: str

    attachment_count: Optional[int] = None

    attachments: Optional[List[Attachment]] = None

    bcc_addresses: Optional[str] = None

    cc_addresses: Optional[str] = None

    document_id: Optional[str] = None

    error_message: Optional[str] = None

    processed: Optional[bool] = None

    processed_at: Optional[datetime] = None

    received_at: Optional[datetime] = None

    sender_name: Optional[str] = None

    subject: Optional[str] = None

    to_addresses: Optional[str] = None
