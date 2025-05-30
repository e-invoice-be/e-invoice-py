# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["PaymentDetailCreate"]


class PaymentDetailCreate(BaseModel):
    bank_account_number: Optional[str] = None

    iban: Optional[str] = None

    payment_reference: Optional[str] = None

    swift: Optional[str] = None
