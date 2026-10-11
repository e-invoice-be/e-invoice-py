from ..._models import BaseModel

__all__ = ["AttachmentDeleteResponse"]


class AttachmentDeleteResponse(BaseModel):
    is_deleted: bool
