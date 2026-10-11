from typing import Dict, List

from .._models import BaseModel

__all__ = ["WebhookRetrieveHistoryResponse"]


class WebhookRetrieveHistoryResponse(BaseModel):
    history: List[Dict[str, object]]
