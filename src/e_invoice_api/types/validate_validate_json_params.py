# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from datetime import date
from typing_extensions import Annotated, TypedDict

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

    tax_details: Optional[Iterable[TaxDetail]]

    total_discount: Union[float, str, None]

    total_tax: Union[float, str, None]

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
