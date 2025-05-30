# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["UblDocumentValidation", "Issue"]


class Issue(BaseModel):
    message: str

    schematron: str

    type: Literal["error", "warning"]

    flag: Optional[str] = None

    location: Optional[str] = None

    rule_id: Optional[str] = None

    test: Optional[str] = None


class UblDocumentValidation(BaseModel):
    id: str

    file_name: Optional[str] = None

    is_valid: bool

    issues: List[Issue]

    ubl_document: Optional[str] = None
