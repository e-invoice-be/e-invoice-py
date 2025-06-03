# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["WebhookResponse"]


class WebhookResponse(BaseModel):
    id: str

    events: List[str]

    secret: str

    url: str

    enabled: Optional[bool] = None
