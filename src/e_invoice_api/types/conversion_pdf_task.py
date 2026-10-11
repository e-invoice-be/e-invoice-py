# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ConversionPdfTask"]


class ConversionPdfTask(BaseModel):
    task_id: str
    """The ID of the task that will process the PDF"""

    status: Optional[Literal["pending", "completed", "failed"]] = None
    """The status of the task"""
