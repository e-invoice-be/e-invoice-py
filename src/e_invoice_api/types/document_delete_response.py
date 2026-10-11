from .._models import BaseModel

__all__ = ["DocumentDeleteResponse"]


class DocumentDeleteResponse(BaseModel):
    is_deleted: bool
