# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["PaymentDetailCreateParam"]


class PaymentDetailCreateParam(TypedDict, total=False):
    bank_account_number: Optional[str]
    """Bank account number (for non-IBAN accounts)"""

    iban: Optional[str]
    """International Bank Account Number for payment transfers"""

    payment_reference: Optional[str]
    """
    Structured payment reference or communication (e.g., structured communication
    for Belgian bank transfers)
    """

    swift: Optional[str]
    """SWIFT/BIC code of the bank"""
