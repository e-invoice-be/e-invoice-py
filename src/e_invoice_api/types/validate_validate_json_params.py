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

__all__ = ["ValidateValidateJsonParams", "Allowance", "Charge", "Item", "ItemAllowance", "ItemCharge", "TaxDetail"]


class ValidateValidateJsonParams(TypedDict, total=False):
    allowances: Optional[Iterable[Allowance]]

    amount_due: Union[float, str, None]
    """The amount due for payment. Must be positive and rounded to maximum 2 decimals"""

    attachments: Optional[Iterable[DocumentAttachmentCreateParam]]

    billing_address: Optional[str]
    """The billing address (if different from customer address)"""

    billing_address_recipient: Optional[str]
    """The recipient name at the billing address"""

    charges: Optional[Iterable[Charge]]

    currency: CurrencyCode
    """Currency of the invoice (ISO 4217 currency code)"""

    customer_address: Optional[str]
    """The address of the customer/buyer"""

    customer_address_recipient: Optional[str]
    """The recipient name at the customer address"""

    customer_company_id: Optional[str]
    """Customer company ID.

    For Belgium this is the CBE number or their EUID (European Unique Identifier)
    number. In the Netherlands this is the KVK number.
    """

    customer_email: Optional[str]
    """The email address of the customer"""

    customer_id: Optional[str]
    """The unique identifier for the customer in your system"""

    customer_name: Optional[str]
    """The company name of the customer/buyer"""

    customer_tax_id: Optional[str]
    """Customer tax ID.

    For Belgium this is the VAT number. Must include the country prefix
    """

    direction: DocumentDirection
    """The direction of the document: INBOUND (purchases) or OUTBOUND (sales)"""

    document_type: DocumentType
    """The type of document: INVOICE, CREDIT_NOTE, or DEBIT_NOTE"""

    due_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """The date when payment is due"""

    invoice_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """The date when the invoice was issued"""

    invoice_id: Optional[str]
    """The unique invoice identifier/number"""

    invoice_total: Union[float, str, None]
    """
    The total amount of the invoice including tax (invoice_total = subtotal +
    total_tax + total_discount). Must be positive and rounded to maximum 2 decimals
    """

    items: Iterable[Item]
    """At least one line item is required"""

    note: Optional[str]
    """Additional notes or comments for the invoice"""

    payment_details: Optional[Iterable[PaymentDetailCreateParam]]

    payment_term: Optional[str]
    """The payment terms (e.g., 'Net 30', 'Due on receipt', '2/10 Net 30')"""

    previous_unpaid_balance: Union[float, str, None]
    """The previous unpaid balance from prior invoices, if any.

    Must be positive and rounded to maximum 2 decimals
    """

    purchase_order: Optional[str]
    """The purchase order reference number"""

    remittance_address: Optional[str]
    """The address where payment should be sent or remitted to"""

    remittance_address_recipient: Optional[str]
    """The recipient name at the remittance address"""

    service_address: Optional[str]
    """The address where services were performed or goods were delivered"""

    service_address_recipient: Optional[str]
    """The recipient name at the service address"""

    service_end_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """The end date of the service period or delivery period"""

    service_start_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """The start date of the service period or delivery period"""

    shipping_address: Optional[str]
    """The shipping/delivery address"""

    shipping_address_recipient: Optional[str]
    """The recipient name at the shipping address"""

    state: DocumentState
    """The current state of the document: DRAFT, TRANSIT, FAILED, SENT, or RECEIVED"""

    subtotal: Union[float, str, None]
    """The taxable base of the invoice.

    Should be the sum of all line items - allowances (for example commercial
    discounts) + charges with impact on VAT. Must be positive and rounded to maximum
    2 decimals
    """

    tax_code: Literal["AE", "E", "S", "Z", "G", "O", "K", "L", "M", "B"]
    """
    Tax category code of the invoice (e.g., S for standard rate, Z for zero rate, E
    for exempt)
    """

    tax_details: Optional[Iterable[TaxDetail]]

    total_discount: Union[float, str, None]
    """
    The net financial discount/charge of the invoice (non-VAT charges minus non-VAT
    allowances). Can be positive (net charge), negative (net discount), or zero.
    Must be rounded to maximum 2 decimals
    """

    total_tax: Union[float, str, None]
    """The total tax amount of the invoice.

    Must be positive and rounded to maximum 2 decimals
    """

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
    """Textual explanation for VAT exemption"""

    vendor_address: Optional[str]
    """The address of the vendor/seller"""

    vendor_address_recipient: Optional[str]
    """The recipient name at the vendor address"""

    vendor_company_id: Optional[str]
    """Vendor company ID.

    For Belgium this is the CBE number or their EUID (European Unique Identifier)
    number. In the Netherlands this is the KVK number.
    """

    vendor_email: Optional[str]
    """The email address of the vendor"""

    vendor_name: Optional[str]
    """The name of the vendor/seller/supplier"""

    vendor_tax_id: Optional[str]
    """Vendor tax ID.

    For Belgium this is the VAT number. Must include the country prefix
    """


class Allowance(TypedDict, total=False):
    amount: Union[float, str, None]
    """The allowance amount, without VAT. Must be rounded to maximum 2 decimals"""

    base_amount: Union[float, str, None]
    """
    The base amount that may be used, in conjunction with the allowance percentage,
    to calculate the allowance amount. Must be rounded to maximum 2 decimals
    """

    multiplier_factor: Union[float, str, None]
    """
    The percentage that may be used, in conjunction with the allowance base amount,
    to calculate the allowance amount. To state 20%, use value 20
    """

    reason: Optional[str]
    """The reason for the allowance"""

    reason_code: Optional[str]
    """The code for the allowance reason"""

    tax_code: Optional[Literal["AE", "E", "S", "Z", "G", "O", "K", "L", "M", "B"]]
    """Duty or tax or fee category codes (Subset of UNCL5305)

    Agency: UN/CEFACT Version: D.16B Subset: OpenPEPPOL
    """

    tax_rate: Optional[str]
    """The VAT rate, represented as percentage that applies to the allowance"""


class Charge(TypedDict, total=False):
    amount: Union[float, str, None]
    """The charge amount, without VAT. Must be rounded to maximum 2 decimals"""

    base_amount: Union[float, str, None]
    """
    The base amount that may be used, in conjunction with the charge percentage, to
    calculate the charge amount. Must be rounded to maximum 2 decimals
    """

    multiplier_factor: Union[float, str, None]
    """
    The percentage that may be used, in conjunction with the charge base amount, to
    calculate the charge amount. To state 20%, use value 20
    """

    reason: Optional[str]
    """The reason for the charge"""

    reason_code: Optional[str]
    """The code for the charge reason"""

    tax_code: Optional[Literal["AE", "E", "S", "Z", "G", "O", "K", "L", "M", "B"]]
    """Duty or tax or fee category codes (Subset of UNCL5305)

    Agency: UN/CEFACT Version: D.16B Subset: OpenPEPPOL
    """

    tax_rate: Optional[str]
    """The VAT rate, represented as percentage that applies to the charge"""


class ItemAllowance(TypedDict, total=False):
    amount: Union[float, str, None]
    """The allowance amount, without VAT. Must be rounded to maximum 2 decimals"""

    base_amount: Union[float, str, None]
    """
    The base amount that may be used, in conjunction with the allowance percentage,
    to calculate the allowance amount. Must be rounded to maximum 2 decimals
    """

    multiplier_factor: Union[float, str, None]
    """
    The percentage that may be used, in conjunction with the allowance base amount,
    to calculate the allowance amount. To state 20%, use value 20
    """

    reason: Optional[str]
    """The reason for the allowance"""

    reason_code: Optional[str]
    """The code for the allowance reason"""

    tax_code: Optional[Literal["AE", "E", "S", "Z", "G", "O", "K", "L", "M", "B"]]
    """Duty or tax or fee category codes (Subset of UNCL5305)

    Agency: UN/CEFACT Version: D.16B Subset: OpenPEPPOL
    """

    tax_rate: Optional[str]
    """The VAT rate, represented as percentage that applies to the allowance"""


class ItemCharge(TypedDict, total=False):
    amount: Union[float, str, None]
    """The charge amount, without VAT. Must be rounded to maximum 2 decimals"""

    base_amount: Union[float, str, None]
    """
    The base amount that may be used, in conjunction with the charge percentage, to
    calculate the charge amount. Must be rounded to maximum 2 decimals
    """

    multiplier_factor: Union[float, str, None]
    """
    The percentage that may be used, in conjunction with the charge base amount, to
    calculate the charge amount. To state 20%, use value 20
    """

    reason: Optional[str]
    """The reason for the charge"""

    reason_code: Optional[str]
    """The code for the charge reason"""

    tax_code: Optional[Literal["AE", "E", "S", "Z", "G", "O", "K", "L", "M", "B"]]
    """Duty or tax or fee category codes (Subset of UNCL5305)

    Agency: UN/CEFACT Version: D.16B Subset: OpenPEPPOL
    """

    tax_rate: Optional[str]
    """The VAT rate, represented as percentage that applies to the charge"""


class Item(TypedDict, total=False):
    allowances: Optional[Iterable[ItemAllowance]]
    """The allowances of the line item."""

    amount: Union[float, str, None]
    """
    The total amount of the line item, exclusive of VAT, after subtracting line
    level allowances and adding line level charges. Must be rounded to maximum 2
    decimals
    """

    charges: Optional[Iterable[ItemCharge]]
    """The charges of the line item."""

    date: None

    description: Optional[str]
    """The description of the line item."""

    product_code: Optional[str]
    """The product code of the line item."""

    quantity: Union[float, str, None]
    """The quantity of items (goods or services) that is the subject of the line item.

    Must be rounded to maximum 4 decimals
    """

    tax: Union[float, str, None]
    """The total VAT amount for the line item. Must be rounded to maximum 2 decimals"""

    tax_rate: Optional[str]
    """The VAT rate of the line item expressed as percentage with 2 decimals"""

    unit: Optional[UnitOfMeasureCode]
    """Unit of Measure Codes from UNECERec20 used in Peppol BIS Billing 3.0."""

    unit_price: Union[float, str, None]
    """The unit price of the line item. Must be rounded to maximum 2 decimals"""


class TaxDetail(TypedDict, total=False):
    amount: Union[float, str, None]
    """The tax amount for this tax category. Must be rounded to maximum 2 decimals"""

    rate: Optional[str]
    """The tax rate as a percentage (e.g., '21.00', '6.00', '0.00')"""
