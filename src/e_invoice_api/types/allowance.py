# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Allowance"]


class Allowance(BaseModel):
    """An allowance is a discount for example for early payment, volume discount, etc."""

    amount: Optional[str] = None
    """The allowance amount, without VAT. Must be rounded to maximum 2 decimals"""

    base_amount: Optional[str] = None
    """
    The base amount that may be used, in conjunction with the allowance percentage,
    to calculate the allowance amount. Must be rounded to maximum 2 decimals
    """

    multiplier_factor: Optional[str] = None
    """
    The percentage that may be used, in conjunction with the allowance base amount,
    to calculate the allowance amount. To state 20%, use value 20. Must be rounded
    to maximum 2 decimals
    """

    reason: Optional[str] = None
    """The reason for the allowance"""

    reason_code: Optional[
        Literal[
            "41",
            "42",
            "60",
            "62",
            "63",
            "64",
            "65",
            "66",
            "67",
            "68",
            "70",
            "71",
            "88",
            "95",
            "100",
            "102",
            "103",
            "104",
            "105",
        ]
    ] = None
    """Allowance reason codes for invoice discounts and charges"""

    tax_code: Optional[Literal["AE", "E", "S", "Z", "G", "O", "K", "L", "M", "B"]] = None
    """The VAT category code that applies to the allowance"""

    tax_rate: Optional[str] = None
    """The VAT rate, represented as percentage that applies to the allowance.

    Must be rounded to maximum 2 decimals
    """
