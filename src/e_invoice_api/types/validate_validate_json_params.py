# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from datetime import date
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo
from .currency_code import CurrencyCode
from .document_type import DocumentType
from .document_state import DocumentState
from .document_direction import DocumentDirection
from .unit_of_measure_code import UnitOfMeasureCode
from .payment_detail_create_param import PaymentDetailCreateParam
from .document_attachment_create_param import DocumentAttachmentCreateParam

__all__ = ["ValidateValidateJsonParams", "Item", "TaxDetail"]


class ValidateValidateJsonParams(TypedDict, total=False):
    amount_due: Union[float, str, None]

    attachments: Optional[Iterable[DocumentAttachmentCreateParam]]

    billing_address: Optional[str]

    billing_address_recipient: Optional[str]

    currency: CurrencyCode
    """Currency of the invoice"""

    customer_address: Optional[str]

    customer_address_recipient: Optional[str]

    customer_email: Optional[str]

    customer_id: Optional[str]

    customer_name: Optional[str]

    customer_tax_id: Optional[str]

    direction: DocumentDirection

    document_type: DocumentType

    due_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]

    invoice_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]

    invoice_id: Optional[str]

    invoice_total: Union[float, str, None]

    items: Optional[Iterable[Item]]

    note: Optional[str]

    payment_details: Optional[Iterable[PaymentDetailCreateParam]]

    payment_term: Optional[str]

    previous_unpaid_balance: Union[float, str, None]

    purchase_order: Optional[str]

    remittance_address: Optional[str]

    remittance_address_recipient: Optional[str]

    service_address: Optional[str]

    service_address_recipient: Optional[str]

    service_end_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]

    service_start_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]

    shipping_address: Optional[str]

    shipping_address_recipient: Optional[str]

    state: DocumentState

    subtotal: Union[float, str, None]

    tax_code: Literal["AE", "E", "S", "Z", "G", "O", "K", "L", "M", "B"]
    """Tax category code of the invoice"""

    tax_details: Optional[Iterable[TaxDetail]]

    total_discount: Union[float, str, None]

    total_tax: Union[float, str, None]

    vatex: Optional[
        Literal[
            "VATEX-EU-79-C",
            "VATEX-EU-132",
            "VATEX-EU-132-1A",
            "VATEX-EU-132-1B",
            "VATEX-EU-132-1C",
            "VATEX-EU-132-1D",
            "VATEX-EU-132-1E",
            "VATEX-EU-132-1F",
            "VATEX-EU-132-1G",
            "VATEX-EU-132-1H",
            "VATEX-EU-132-1I",
            "VATEX-EU-132-1J",
            "VATEX-EU-132-1K",
            "VATEX-EU-132-1L",
            "VATEX-EU-132-1M",
            "VATEX-EU-132-1N",
            "VATEX-EU-132-1O",
            "VATEX-EU-132-1P",
            "VATEX-EU-132-1Q",
            "VATEX-EU-143",
            "VATEX-EU-143-1A",
            "VATEX-EU-143-1B",
            "VATEX-EU-143-1C",
            "VATEX-EU-143-1D",
            "VATEX-EU-143-1E",
            "VATEX-EU-143-1F",
            "VATEX-EU-143-1FA",
            "VATEX-EU-143-1G",
            "VATEX-EU-143-1H",
            "VATEX-EU-143-1I",
            "VATEX-EU-143-1J",
            "VATEX-EU-143-1K",
            "VATEX-EU-143-1L",
            "VATEX-EU-144",
            "VATEX-EU-146-1E",
            "VATEX-EU-148",
            "VATEX-EU-148-A",
            "VATEX-EU-148-B",
            "VATEX-EU-148-C",
            "VATEX-EU-148-D",
            "VATEX-EU-148-E",
            "VATEX-EU-148-F",
            "VATEX-EU-148-G",
            "VATEX-EU-151",
            "VATEX-EU-151-1A",
            "VATEX-EU-151-1AA",
            "VATEX-EU-151-1B",
            "VATEX-EU-151-1C",
            "VATEX-EU-151-1D",
            "VATEX-EU-151-1E",
            "VATEX-EU-159",
            "VATEX-EU-309",
            "VATEX-EU-AE",
            "VATEX-EU-D",
            "VATEX-EU-F",
            "VATEX-EU-G",
            "VATEX-EU-I",
            "VATEX-EU-IC",
            "VATEX-EU-O",
            "VATEX-EU-J",
            "VATEX-FR-FRANCHISE",
            "VATEX-FR-CNWVAT",
        ]
    ]
    """VATEX code list for VAT exemption reasons

    Agency: CEF Identifier: vatex
    """

    vatex_note: Optional[str]
    """VAT exemption note of the invoice"""

    vendor_address: Optional[str]

    vendor_address_recipient: Optional[str]

    vendor_email: Optional[str]

    vendor_name: Optional[str]

    vendor_tax_id: Optional[str]


class Item(TypedDict, total=False):
    amount: Union[float, str, None]

    date: None

    description: Optional[str]

    product_code: Optional[str]

    quantity: Union[float, str, None]

    tax: Union[float, str, None]

    tax_rate: Optional[str]

    unit: Optional[UnitOfMeasureCode]
    """Unit of Measure Codes from UNECERec20 used in Peppol BIS Billing 3.0."""

    unit_price: Union[float, str, None]


class TaxDetail(TypedDict, total=False):
    amount: Union[float, str, None]

    rate: Optional[str]
