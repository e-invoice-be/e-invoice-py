# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import date
from typing_extensions import Literal

from .._models import BaseModel
from .currency_code import CurrencyCode
from .document_type import DocumentType
from .document_state import DocumentState
from .document_direction import DocumentDirection
from .unit_of_measure_code import UnitOfMeasureCode
from .documents.document_attachment import DocumentAttachment

__all__ = ["DocumentResponse", "Item", "PaymentDetail", "TaxDetail"]


class Item(BaseModel):
    amount: Optional[str] = None

    date: None = None

    description: Optional[str] = None

    product_code: Optional[str] = None

    quantity: Optional[str] = None

    tax: Optional[str] = None

    tax_rate: Optional[str] = None

    unit: Optional[UnitOfMeasureCode] = None
    """Unit of Measure Codes from UNECERec20 used in Peppol BIS Billing 3.0."""

    unit_price: Optional[str] = None


class PaymentDetail(BaseModel):
    bank_account_number: Optional[str] = None

    iban: Optional[str] = None

    payment_reference: Optional[str] = None

    swift: Optional[str] = None


class TaxDetail(BaseModel):
    amount: Optional[str] = None

    rate: Optional[str] = None


class DocumentResponse(BaseModel):
    id: str

    amount_due: Optional[str] = None

    attachments: Optional[List[DocumentAttachment]] = None

    billing_address: Optional[str] = None

    billing_address_recipient: Optional[str] = None

    currency: Optional[CurrencyCode] = None
    """Currency of the invoice"""

    customer_address: Optional[str] = None

    customer_address_recipient: Optional[str] = None

    customer_email: Optional[str] = None

    customer_id: Optional[str] = None

    customer_name: Optional[str] = None

    customer_tax_id: Optional[str] = None

    direction: Optional[DocumentDirection] = None

    document_type: Optional[DocumentType] = None

    due_date: Optional[date] = None

    invoice_date: Optional[date] = None

    invoice_id: Optional[str] = None

    invoice_total: Optional[str] = None

    items: Optional[List[Item]] = None

    note: Optional[str] = None

    payment_details: Optional[List[PaymentDetail]] = None

    payment_term: Optional[str] = None

    previous_unpaid_balance: Optional[str] = None

    purchase_order: Optional[str] = None

    remittance_address: Optional[str] = None

    remittance_address_recipient: Optional[str] = None

    service_address: Optional[str] = None

    service_address_recipient: Optional[str] = None

    service_end_date: Optional[date] = None

    service_start_date: Optional[date] = None

    shipping_address: Optional[str] = None

    shipping_address_recipient: Optional[str] = None

    state: Optional[DocumentState] = None

    subtotal: Optional[str] = None

    tax_code: Optional[Literal["AE", "E", "S", "Z", "G", "O", "K", "L", "M", "B"]] = None
    """Tax category code of the invoice"""

    tax_details: Optional[List[TaxDetail]] = None

    total_discount: Optional[str] = None

    total_tax: Optional[str] = None

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
    ] = None
    """VATEX code list for VAT exemption reasons

    Agency: CEF Identifier: vatex
    """

    vatex_note: Optional[str] = None
    """VAT exemption note of the invoice"""

    vendor_address: Optional[str] = None

    vendor_address_recipient: Optional[str] = None

    vendor_email: Optional[str] = None

    vendor_name: Optional[str] = None

    vendor_tax_id: Optional[str] = None
