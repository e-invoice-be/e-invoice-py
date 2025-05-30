# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["PaymentDetailCreateParam"]


class PaymentDetailCreateParam(TypedDict, total=False):
    bank_account_number: Optional[str]

    iban: Optional[str]

    payment_reference: Optional[str]

    swift: Optional[str]
