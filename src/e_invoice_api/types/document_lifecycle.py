from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["DocumentLifecycle", "Event"]


class Event(BaseModel):
    canonical_status: Optional[
        Literal[
            "deposited",
            "emitted",
            "delivered",
            "rejected",
            "acknowledged",
            "approved",
            "partially_approved",
            "disputed",
            "on_hold",
            "refused",
            "payment_sent",
            "paid",
        ]
    ] = None

    direction: Literal["in", "out"]

    level: Literal["transport", "business"]

    native_code: Optional[str] = None

    occurred_at: datetime

    reason: Optional[str] = None

    reason_code: Optional[str] = None

    source: Literal["peppol:mlr", "peppol:mls", "peppol:imr", "fr:superpdp", "local"]


class DocumentLifecycle(BaseModel):
    document_id: str

    events: List[Event]
