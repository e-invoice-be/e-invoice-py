# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["PaymentDetailCreate"]


class PaymentDetailCreate(BaseModel):
    bank_account_number: Optional[str] = None
    """Bank account number (for non-IBAN accounts)"""

    iban: Optional[str] = None
    """International Bank Account Number for payment transfers"""

    payment_reference: Optional[str] = None
    """
    Structured payment reference or communication (e.g., structured communication
    for Belgian bank transfers)
    """

    swift: Optional[str] = None
    """SWIFT/BIC code of the bank"""
