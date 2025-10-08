# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Charge"]


class Charge(BaseModel):
    amount: Optional[str] = None
    """The charge amount, without VAT. Must be rounded to maximum 2 decimals"""

    base_amount: Optional[str] = None
    """
    The base amount that may be used, in conjunction with the charge percentage, to
    calculate the charge amount. Must be rounded to maximum 2 decimals
    """

    multiplier_factor: Optional[str] = None
    """
    The percentage that may be used, in conjunction with the charge base amount, to
    calculate the charge amount. To state 20%, use value 20
    """

    reason: Optional[str] = None
    """The reason for the charge"""

    reason_code: Optional[str] = None
    """The code for the charge reason"""

    tax_code: Optional[Literal["AE", "E", "S", "Z", "G", "O", "K", "L", "M", "B"]] = None
    """Duty or tax or fee category codes (Subset of UNCL5305)

    Agency: UN/CEFACT Version: D.16B Subset: OpenPEPPOL
    """

    tax_rate: Optional[str] = None
    """The VAT rate, represented as percentage that applies to the charge"""
