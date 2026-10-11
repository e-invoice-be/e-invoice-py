from typing import Dict

from .._models import BaseModel

__all__ = ["WebhookTestResponse"]


class WebhookTestResponse(BaseModel):
    """Schema for webhook test response."""

    message: str
    """Descriptive message about the test result"""

    success: bool
    """Whether the test completed successfully"""

    webhook_delivery_result: Dict[str, object]
    """Result from process_webhook_task"""
