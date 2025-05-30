# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .._models import BaseModel

__all__ = ["Certificate"]


class Certificate(BaseModel):
    status: str
    """Status of the certificate validation: 'success', 'error', or 'pending'"""

    details: Optional[Dict[str, object]] = None
    """Details about the certificate including subject, issuer, validity dates, etc."""

    error: Optional[str] = None
    """Error message if certificate validation failed"""
