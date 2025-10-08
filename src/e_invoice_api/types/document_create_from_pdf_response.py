# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import date
from typing_extensions import Literal

from .charge import Charge
from .._models import BaseModel
from .allowance import Allowance
from .currency_code import CurrencyCode
from .document_type import DocumentType
from .document_state import DocumentState
from .document_direction import DocumentDirection
from .unit_of_measure_code import UnitOfMeasureCode
from .payment_detail_create import PaymentDetailCreate
from .document_attachment_create import DocumentAttachmentCreate

__all__ = ["DocumentCreateFromPdfResponse", "Item", "TaxDetail"]


class Item(BaseModel):
    allowances: Optional[List[Allowance]] = None
    """The allowances of the line item."""

    amount: Optional[str] = None
    """
    The total amount of the line item, exclusive of VAT, after subtracting line
    level allowances and adding line level charges. Must be rounded to maximum 2
    decimals
    """

    charges: Optional[List[Charge]] = None
    """The charges of the line item."""

    date: None = None

    description: Optional[str] = None
    """The description of the line item."""

    product_code: Optional[str] = None
    """The product code of the line item."""

    quantity: Optional[str] = None
    """The quantity of items (goods or services) that is the subject of the line item.

    Must be rounded to maximum 4 decimals
    """

    tax: Optional[str] = None
    """The total VAT amount for the line item. Must be rounded to maximum 2 decimals"""

    tax_rate: Optional[str] = None
    """The VAT rate of the line item expressed as percentage with 2 decimals"""

    unit: Optional[UnitOfMeasureCode] = None
    """Unit of Measure Codes from UNECERec20 used in Peppol BIS Billing 3.0."""

    unit_price: Optional[str] = None
    """The unit price of the line item. Must be rounded to maximum 2 decimals"""


class TaxDetail(BaseModel):
    amount: Optional[str] = None

    rate: Optional[str] = None


class DocumentCreateFromPdfResponse(BaseModel):
    allowances: Optional[List[Allowance]] = None

    amount_due: Optional[str] = None
    """The amount due of the invoice.

    Must be positive and rounded to maximum 2 decimals
    """

    attachments: Optional[List[DocumentAttachmentCreate]] = None

    billing_address: Optional[str] = None

    billing_address_recipient: Optional[str] = None

    charges: Optional[List[Charge]] = None

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
    """
    The total amount of the invoice (so invoice_total = subtotal + total_tax +
    total_discount). Must be positive and rounded to maximum 2 decimals
    """

    items: Optional[List[Item]] = None
    """At least one line item is required"""

    note: Optional[str] = None

    payment_details: Optional[List[PaymentDetailCreate]] = None

    payment_term: Optional[str] = None

    previous_unpaid_balance: Optional[str] = None
    """The previous unpaid balance of the invoice, if any.

    Must be positive and rounded to maximum 2 decimals
    """

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
    """The taxable base of the invoice.

    Should be the sum of all line items - allowances (for example commercial
    discounts) + charges with impact on VAT. Must be positive and rounded to maximum
    2 decimals
    """

    success: Optional[bool] = None
    """Whether the PDF was successfully converted into a compliant e-invoice"""

    tax_code: Optional[Literal["AE", "E", "S", "Z", "G", "O", "K", "L", "M", "B"]] = None
    """Tax category code of the invoice"""

    tax_details: Optional[List[TaxDetail]] = None

    total_discount: Optional[str] = None
    """The total financial discount of the invoice (so discounts not subject to VAT).

    Must be positive and rounded to maximum 2 decimals
    """

    total_tax: Optional[str] = None
    """The total tax of the invoice.

    Must be positive and rounded to maximum 2 decimals
    """

    ubl_document: Optional[str] = None
    """The UBL document as an XML string"""

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
