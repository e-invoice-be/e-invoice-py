from .._models import BaseModel

__all__ = ["WebhookDeleteResponse"]


class WebhookDeleteResponse(BaseModel):
    """Model for webhook deletion."""

    is_deleted: bool
