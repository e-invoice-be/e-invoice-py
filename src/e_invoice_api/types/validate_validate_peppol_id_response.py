# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import date

from .._models import BaseModel

__all__ = ["ValidateValidatePeppolIDResponse", "BusinessCard"]


class BusinessCard(BaseModel):
    country_code: Optional[str] = None

    name: Optional[str] = None

    registration_date: Optional[date] = None


class ValidateValidatePeppolIDResponse(BaseModel):
    business_card: Optional[BusinessCard] = None
    """Business card information for the Peppol ID"""

    business_card_valid: bool
    """Whether a business card is set at the SMP"""

    dns_valid: bool
    """Whether the DNS resolves to a valid SMP"""

    is_valid: bool
    """Whether the Peppol ID is valid and registered in the Peppol network"""

    supported_document_types: Optional[List[str]] = None
