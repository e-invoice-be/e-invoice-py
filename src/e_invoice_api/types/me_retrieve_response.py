# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["MeRetrieveResponse"]


class MeRetrieveResponse(BaseModel):
    credit_balance: int
    """Credit balance of the tenant"""

    name: str

    plan: Literal["starter", "pro", "enterprise"]
    """Plan of the tenant"""

    description: Optional[str] = None

    ibans: Optional[List[str]] = None
    """IBANs of the tenant"""

    peppol_ids: Optional[List[str]] = None
    """Peppol IDs of the tenant"""
