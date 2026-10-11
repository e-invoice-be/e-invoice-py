from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["DocumentTimeline", "Event"]


class Event(BaseModel):
    event_type: Literal[
        "email_received",
        "email_processed",
        "document_created",
        "send_attempted",
        "send_failed",
        "send_success",
        "receive_success",
        "mlr_received",
        "imr_received",
    ]

    timestamp: datetime

    id: Optional[str] = None

    details: Optional[Dict[str, object]] = None


class DocumentTimeline(BaseModel):
    document_id: str

    events: List[Event]
