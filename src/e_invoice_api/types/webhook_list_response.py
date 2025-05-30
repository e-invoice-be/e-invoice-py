# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .webhook_response import WebhookResponse

__all__ = ["WebhookListResponse"]

WebhookListResponse: TypeAlias = List[WebhookResponse]
