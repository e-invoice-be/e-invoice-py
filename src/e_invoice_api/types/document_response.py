# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import date

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

    tax_details: Optional[List[TaxDetail]] = None

    total_discount: Optional[str] = None

    total_tax: Optional[str] = None

    vendor_address: Optional[str] = None

    vendor_address_recipient: Optional[str] = None

    vendor_email: Optional[str] = None

    vendor_name: Optional[str] = None

    vendor_tax_id: Optional[str] = None
