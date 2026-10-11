from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["WebhookTestParams"]


class WebhookTestParams(TypedDict, total=False):
    data: Required[Dict[str, object]]
    """Custom event data payload"""

    event_type: Required[str]
    """Must be valid WebhookEventType"""
