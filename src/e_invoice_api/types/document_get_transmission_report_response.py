# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = ["DocumentGetTransmissionReportResponse", "DocumentGetTransmissionReportResponseItem"]


class DocumentGetTransmissionReportResponseItem(BaseModel):
    id: str

    channel: str

    created_at: datetime

    delivery_address: str

    document_id: str

    status: Literal["PENDING", "SUCCESS", "FAILED"]

    transmission_type: Literal["SEND", "RECEIVE"]

    updated_at: datetime

    data: Optional[Dict[str, object]] = None

    error: Optional[str] = None


DocumentGetTransmissionReportResponse: TypeAlias = List[DocumentGetTransmissionReportResponseItem]
