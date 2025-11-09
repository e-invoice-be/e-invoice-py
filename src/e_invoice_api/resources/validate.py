# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Mapping, Iterable, Optional, cast
from datetime import date
from typing_extensions import Literal

import httpx

from ..types import (
    CurrencyCode,
    DocumentType,
    DocumentState,
    DocumentDirection,
    validate_validate_ubl_params,
    validate_validate_json_params,
    validate_validate_peppol_id_params,
)
from .._types import Body, Omit, Query, Headers, NotGiven, FileTypes, omit, not_given
from .._utils import extract_files, maybe_transform, deepcopy_minimal, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.currency_code import CurrencyCode
from ..types.document_type import DocumentType
from ..types.document_state import DocumentState
from ..types.document_direction import DocumentDirection
from ..types.ubl_document_validation import UblDocumentValidation
from ..types.payment_detail_create_param import PaymentDetailCreateParam
from ..types.document_attachment_create_param import DocumentAttachmentCreateParam
from ..types.validate_validate_peppol_id_response import ValidateValidatePeppolIDResponse

__all__ = ["ValidateResource", "AsyncValidateResource"]


class ValidateResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ValidateResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return ValidateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ValidateResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return ValidateResourceWithStreamingResponse(self)

    def validate_json(
        self,
        *,
        allowances: Optional[Iterable[validate_validate_json_params.Allowance]] | Omit = omit,
        amount_due: Union[float, str, None] | Omit = omit,
        attachments: Optional[Iterable[DocumentAttachmentCreateParam]] | Omit = omit,
        billing_address: Optional[str] | Omit = omit,
        billing_address_recipient: Optional[str] | Omit = omit,
        charges: Optional[Iterable[validate_validate_json_params.Charge]] | Omit = omit,
        currency: CurrencyCode | Omit = omit,
        customer_address: Optional[str] | Omit = omit,
        customer_address_recipient: Optional[str] | Omit = omit,
        customer_company_id: Optional[str] | Omit = omit,
        customer_email: Optional[str] | Omit = omit,
        customer_id: Optional[str] | Omit = omit,
        customer_name: Optional[str] | Omit = omit,
        customer_tax_id: Optional[str] | Omit = omit,
        direction: DocumentDirection | Omit = omit,
        document_type: DocumentType | Omit = omit,
        due_date: Union[str, date, None] | Omit = omit,
        invoice_date: Union[str, date, None] | Omit = omit,
        invoice_id: Optional[str] | Omit = omit,
        invoice_total: Union[float, str, None] | Omit = omit,
        items: Iterable[validate_validate_json_params.Item] | Omit = omit,
        note: Optional[str] | Omit = omit,
        payment_details: Optional[Iterable[PaymentDetailCreateParam]] | Omit = omit,
        payment_term: Optional[str] | Omit = omit,
        previous_unpaid_balance: Union[float, str, None] | Omit = omit,
        purchase_order: Optional[str] | Omit = omit,
        remittance_address: Optional[str] | Omit = omit,
        remittance_address_recipient: Optional[str] | Omit = omit,
        service_address: Optional[str] | Omit = omit,
        service_address_recipient: Optional[str] | Omit = omit,
        service_end_date: Union[str, date, None] | Omit = omit,
        service_start_date: Union[str, date, None] | Omit = omit,
        shipping_address: Optional[str] | Omit = omit,
        shipping_address_recipient: Optional[str] | Omit = omit,
        state: DocumentState | Omit = omit,
        subtotal: Union[float, str, None] | Omit = omit,
        tax_code: Literal["AE", "E", "S", "Z", "G", "O", "K", "L", "M", "B"] | Omit = omit,
        tax_details: Optional[Iterable[validate_validate_json_params.TaxDetail]] | Omit = omit,
        total_discount: Union[float, str, None] | Omit = omit,
        total_tax: Union[float, str, None] | Omit = omit,
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
        | Omit = omit,
        vatex_note: Optional[str] | Omit = omit,
        vendor_address: Optional[str] | Omit = omit,
        vendor_address_recipient: Optional[str] | Omit = omit,
        vendor_company_id: Optional[str] | Omit = omit,
        vendor_email: Optional[str] | Omit = omit,
        vendor_name: Optional[str] | Omit = omit,
        vendor_tax_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UblDocumentValidation:
        """
        Validate if the JSON document can be converted to a valid UBL document

        Args:
          amount_due: The amount due for payment. Must be positive and rounded to maximum 2 decimals

          billing_address: The billing address (if different from customer address)

          billing_address_recipient: The recipient name at the billing address

          currency: Currency of the invoice (ISO 4217 currency code)

          customer_address: The address of the customer/buyer

          customer_address_recipient: The recipient name at the customer address

          customer_company_id: Customer company ID. For Belgium this is the CBE number or their EUID (European
              Unique Identifier) number. In the Netherlands this is the KVK number.

          customer_email: The email address of the customer

          customer_id: The unique identifier for the customer in your system

          customer_name: The company name of the customer/buyer

          customer_tax_id: Customer tax ID. For Belgium this is the VAT number. Must include the country
              prefix

          direction: The direction of the document: INBOUND (purchases) or OUTBOUND (sales)

          document_type: The type of document: INVOICE, CREDIT_NOTE, or DEBIT_NOTE

          due_date: The date when payment is due

          invoice_date: The date when the invoice was issued

          invoice_id: The unique invoice identifier/number

          invoice_total: The total amount of the invoice including tax (invoice_total = subtotal +
              total_tax + total_discount). Must be positive and rounded to maximum 2 decimals

          items: At least one line item is required

          note: Additional notes or comments for the invoice

          payment_term: The payment terms (e.g., 'Net 30', 'Due on receipt', '2/10 Net 30')

          previous_unpaid_balance: The previous unpaid balance from prior invoices, if any. Must be positive and
              rounded to maximum 2 decimals

          purchase_order: The purchase order reference number

          remittance_address: The address where payment should be sent or remitted to

          remittance_address_recipient: The recipient name at the remittance address

          service_address: The address where services were performed or goods were delivered

          service_address_recipient: The recipient name at the service address

          service_end_date: The end date of the service period or delivery period

          service_start_date: The start date of the service period or delivery period

          shipping_address: The shipping/delivery address

          shipping_address_recipient: The recipient name at the shipping address

          state: The current state of the document: DRAFT, TRANSIT, FAILED, SENT, or RECEIVED

          subtotal: The taxable base of the invoice. Should be the sum of all line items -
              allowances (for example commercial discounts) + charges with impact on VAT. Must
              be positive and rounded to maximum 2 decimals

          tax_code: Tax category code of the invoice (e.g., S for standard rate, Z for zero rate, E
              for exempt)

          total_discount: The net financial discount/charge of the invoice (non-VAT charges minus non-VAT
              allowances). Can be positive (net charge), negative (net discount), or zero.
              Must be rounded to maximum 2 decimals

          total_tax: The total tax amount of the invoice. Must be positive and rounded to maximum 2
              decimals

          vatex: VATEX code list for VAT exemption reasons

              Agency: CEF Identifier: vatex

          vatex_note: Textual explanation for VAT exemption

          vendor_address: The address of the vendor/seller

          vendor_address_recipient: The recipient name at the vendor address

          vendor_company_id: Vendor company ID. For Belgium this is the CBE number or their EUID (European
              Unique Identifier) number. In the Netherlands this is the KVK number.

          vendor_email: The email address of the vendor

          vendor_name: The name of the vendor/seller/supplier

          vendor_tax_id: Vendor tax ID. For Belgium this is the VAT number. Must include the country
              prefix

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/validate/json",
            body=maybe_transform(
                {
                    "allowances": allowances,
                    "amount_due": amount_due,
                    "attachments": attachments,
                    "billing_address": billing_address,
                    "billing_address_recipient": billing_address_recipient,
                    "charges": charges,
                    "currency": currency,
                    "customer_address": customer_address,
                    "customer_address_recipient": customer_address_recipient,
                    "customer_company_id": customer_company_id,
                    "customer_email": customer_email,
                    "customer_id": customer_id,
                    "customer_name": customer_name,
                    "customer_tax_id": customer_tax_id,
                    "direction": direction,
                    "document_type": document_type,
                    "due_date": due_date,
                    "invoice_date": invoice_date,
                    "invoice_id": invoice_id,
                    "invoice_total": invoice_total,
                    "items": items,
                    "note": note,
                    "payment_details": payment_details,
                    "payment_term": payment_term,
                    "previous_unpaid_balance": previous_unpaid_balance,
                    "purchase_order": purchase_order,
                    "remittance_address": remittance_address,
                    "remittance_address_recipient": remittance_address_recipient,
                    "service_address": service_address,
                    "service_address_recipient": service_address_recipient,
                    "service_end_date": service_end_date,
                    "service_start_date": service_start_date,
                    "shipping_address": shipping_address,
                    "shipping_address_recipient": shipping_address_recipient,
                    "state": state,
                    "subtotal": subtotal,
                    "tax_code": tax_code,
                    "tax_details": tax_details,
                    "total_discount": total_discount,
                    "total_tax": total_tax,
                    "vatex": vatex,
                    "vatex_note": vatex_note,
                    "vendor_address": vendor_address,
                    "vendor_address_recipient": vendor_address_recipient,
                    "vendor_company_id": vendor_company_id,
                    "vendor_email": vendor_email,
                    "vendor_name": vendor_name,
                    "vendor_tax_id": vendor_tax_id,
                },
                validate_validate_json_params.ValidateValidateJsonParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UblDocumentValidation,
        )

    def validate_peppol_id(
        self,
        *,
        peppol_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ValidateValidatePeppolIDResponse:
        """
        Validate if a Peppol ID exists in the Peppol network and retrieve supported
        document types. The peppol_id must be in the form of `<scheme>:<id>`. The scheme
        is a 4-digit code representing the identifier scheme, and the id is the actual
        identifier value. For example, for a Belgian company it is `0208:0123456789`
        (where 0208 is the scheme for Belgian enterprises, followed by the 10 digits of
        the official BTW / KBO number).

        Args:
          peppol_id: Peppol ID in the format `<scheme>:<id>`. Example: `0208:1018265814` for a
              Belgian company.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/validate/peppol-id",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"peppol_id": peppol_id}, validate_validate_peppol_id_params.ValidateValidatePeppolIDParams
                ),
            ),
            cast_to=ValidateValidatePeppolIDResponse,
        )

    def validate_ubl(
        self,
        *,
        file: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UblDocumentValidation:
        """
        Validate the correctness of a UBL document

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal({"file": file})
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/api/validate/ubl",
            body=maybe_transform(body, validate_validate_ubl_params.ValidateValidateUblParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UblDocumentValidation,
        )


class AsyncValidateResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncValidateResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return AsyncValidateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncValidateResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return AsyncValidateResourceWithStreamingResponse(self)

    async def validate_json(
        self,
        *,
        allowances: Optional[Iterable[validate_validate_json_params.Allowance]] | Omit = omit,
        amount_due: Union[float, str, None] | Omit = omit,
        attachments: Optional[Iterable[DocumentAttachmentCreateParam]] | Omit = omit,
        billing_address: Optional[str] | Omit = omit,
        billing_address_recipient: Optional[str] | Omit = omit,
        charges: Optional[Iterable[validate_validate_json_params.Charge]] | Omit = omit,
        currency: CurrencyCode | Omit = omit,
        customer_address: Optional[str] | Omit = omit,
        customer_address_recipient: Optional[str] | Omit = omit,
        customer_company_id: Optional[str] | Omit = omit,
        customer_email: Optional[str] | Omit = omit,
        customer_id: Optional[str] | Omit = omit,
        customer_name: Optional[str] | Omit = omit,
        customer_tax_id: Optional[str] | Omit = omit,
        direction: DocumentDirection | Omit = omit,
        document_type: DocumentType | Omit = omit,
        due_date: Union[str, date, None] | Omit = omit,
        invoice_date: Union[str, date, None] | Omit = omit,
        invoice_id: Optional[str] | Omit = omit,
        invoice_total: Union[float, str, None] | Omit = omit,
        items: Iterable[validate_validate_json_params.Item] | Omit = omit,
        note: Optional[str] | Omit = omit,
        payment_details: Optional[Iterable[PaymentDetailCreateParam]] | Omit = omit,
        payment_term: Optional[str] | Omit = omit,
        previous_unpaid_balance: Union[float, str, None] | Omit = omit,
        purchase_order: Optional[str] | Omit = omit,
        remittance_address: Optional[str] | Omit = omit,
        remittance_address_recipient: Optional[str] | Omit = omit,
        service_address: Optional[str] | Omit = omit,
        service_address_recipient: Optional[str] | Omit = omit,
        service_end_date: Union[str, date, None] | Omit = omit,
        service_start_date: Union[str, date, None] | Omit = omit,
        shipping_address: Optional[str] | Omit = omit,
        shipping_address_recipient: Optional[str] | Omit = omit,
        state: DocumentState | Omit = omit,
        subtotal: Union[float, str, None] | Omit = omit,
        tax_code: Literal["AE", "E", "S", "Z", "G", "O", "K", "L", "M", "B"] | Omit = omit,
        tax_details: Optional[Iterable[validate_validate_json_params.TaxDetail]] | Omit = omit,
        total_discount: Union[float, str, None] | Omit = omit,
        total_tax: Union[float, str, None] | Omit = omit,
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
        | Omit = omit,
        vatex_note: Optional[str] | Omit = omit,
        vendor_address: Optional[str] | Omit = omit,
        vendor_address_recipient: Optional[str] | Omit = omit,
        vendor_company_id: Optional[str] | Omit = omit,
        vendor_email: Optional[str] | Omit = omit,
        vendor_name: Optional[str] | Omit = omit,
        vendor_tax_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UblDocumentValidation:
        """
        Validate if the JSON document can be converted to a valid UBL document

        Args:
          amount_due: The amount due for payment. Must be positive and rounded to maximum 2 decimals

          billing_address: The billing address (if different from customer address)

          billing_address_recipient: The recipient name at the billing address

          currency: Currency of the invoice (ISO 4217 currency code)

          customer_address: The address of the customer/buyer

          customer_address_recipient: The recipient name at the customer address

          customer_company_id: Customer company ID. For Belgium this is the CBE number or their EUID (European
              Unique Identifier) number. In the Netherlands this is the KVK number.

          customer_email: The email address of the customer

          customer_id: The unique identifier for the customer in your system

          customer_name: The company name of the customer/buyer

          customer_tax_id: Customer tax ID. For Belgium this is the VAT number. Must include the country
              prefix

          direction: The direction of the document: INBOUND (purchases) or OUTBOUND (sales)

          document_type: The type of document: INVOICE, CREDIT_NOTE, or DEBIT_NOTE

          due_date: The date when payment is due

          invoice_date: The date when the invoice was issued

          invoice_id: The unique invoice identifier/number

          invoice_total: The total amount of the invoice including tax (invoice_total = subtotal +
              total_tax + total_discount). Must be positive and rounded to maximum 2 decimals

          items: At least one line item is required

          note: Additional notes or comments for the invoice

          payment_term: The payment terms (e.g., 'Net 30', 'Due on receipt', '2/10 Net 30')

          previous_unpaid_balance: The previous unpaid balance from prior invoices, if any. Must be positive and
              rounded to maximum 2 decimals

          purchase_order: The purchase order reference number

          remittance_address: The address where payment should be sent or remitted to

          remittance_address_recipient: The recipient name at the remittance address

          service_address: The address where services were performed or goods were delivered

          service_address_recipient: The recipient name at the service address

          service_end_date: The end date of the service period or delivery period

          service_start_date: The start date of the service period or delivery period

          shipping_address: The shipping/delivery address

          shipping_address_recipient: The recipient name at the shipping address

          state: The current state of the document: DRAFT, TRANSIT, FAILED, SENT, or RECEIVED

          subtotal: The taxable base of the invoice. Should be the sum of all line items -
              allowances (for example commercial discounts) + charges with impact on VAT. Must
              be positive and rounded to maximum 2 decimals

          tax_code: Tax category code of the invoice (e.g., S for standard rate, Z for zero rate, E
              for exempt)

          total_discount: The net financial discount/charge of the invoice (non-VAT charges minus non-VAT
              allowances). Can be positive (net charge), negative (net discount), or zero.
              Must be rounded to maximum 2 decimals

          total_tax: The total tax amount of the invoice. Must be positive and rounded to maximum 2
              decimals

          vatex: VATEX code list for VAT exemption reasons

              Agency: CEF Identifier: vatex

          vatex_note: Textual explanation for VAT exemption

          vendor_address: The address of the vendor/seller

          vendor_address_recipient: The recipient name at the vendor address

          vendor_company_id: Vendor company ID. For Belgium this is the CBE number or their EUID (European
              Unique Identifier) number. In the Netherlands this is the KVK number.

          vendor_email: The email address of the vendor

          vendor_name: The name of the vendor/seller/supplier

          vendor_tax_id: Vendor tax ID. For Belgium this is the VAT number. Must include the country
              prefix

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/validate/json",
            body=await async_maybe_transform(
                {
                    "allowances": allowances,
                    "amount_due": amount_due,
                    "attachments": attachments,
                    "billing_address": billing_address,
                    "billing_address_recipient": billing_address_recipient,
                    "charges": charges,
                    "currency": currency,
                    "customer_address": customer_address,
                    "customer_address_recipient": customer_address_recipient,
                    "customer_company_id": customer_company_id,
                    "customer_email": customer_email,
                    "customer_id": customer_id,
                    "customer_name": customer_name,
                    "customer_tax_id": customer_tax_id,
                    "direction": direction,
                    "document_type": document_type,
                    "due_date": due_date,
                    "invoice_date": invoice_date,
                    "invoice_id": invoice_id,
                    "invoice_total": invoice_total,
                    "items": items,
                    "note": note,
                    "payment_details": payment_details,
                    "payment_term": payment_term,
                    "previous_unpaid_balance": previous_unpaid_balance,
                    "purchase_order": purchase_order,
                    "remittance_address": remittance_address,
                    "remittance_address_recipient": remittance_address_recipient,
                    "service_address": service_address,
                    "service_address_recipient": service_address_recipient,
                    "service_end_date": service_end_date,
                    "service_start_date": service_start_date,
                    "shipping_address": shipping_address,
                    "shipping_address_recipient": shipping_address_recipient,
                    "state": state,
                    "subtotal": subtotal,
                    "tax_code": tax_code,
                    "tax_details": tax_details,
                    "total_discount": total_discount,
                    "total_tax": total_tax,
                    "vatex": vatex,
                    "vatex_note": vatex_note,
                    "vendor_address": vendor_address,
                    "vendor_address_recipient": vendor_address_recipient,
                    "vendor_company_id": vendor_company_id,
                    "vendor_email": vendor_email,
                    "vendor_name": vendor_name,
                    "vendor_tax_id": vendor_tax_id,
                },
                validate_validate_json_params.ValidateValidateJsonParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UblDocumentValidation,
        )

    async def validate_peppol_id(
        self,
        *,
        peppol_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ValidateValidatePeppolIDResponse:
        """
        Validate if a Peppol ID exists in the Peppol network and retrieve supported
        document types. The peppol_id must be in the form of `<scheme>:<id>`. The scheme
        is a 4-digit code representing the identifier scheme, and the id is the actual
        identifier value. For example, for a Belgian company it is `0208:0123456789`
        (where 0208 is the scheme for Belgian enterprises, followed by the 10 digits of
        the official BTW / KBO number).

        Args:
          peppol_id: Peppol ID in the format `<scheme>:<id>`. Example: `0208:1018265814` for a
              Belgian company.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/validate/peppol-id",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"peppol_id": peppol_id}, validate_validate_peppol_id_params.ValidateValidatePeppolIDParams
                ),
            ),
            cast_to=ValidateValidatePeppolIDResponse,
        )

    async def validate_ubl(
        self,
        *,
        file: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UblDocumentValidation:
        """
        Validate the correctness of a UBL document

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal({"file": file})
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/api/validate/ubl",
            body=await async_maybe_transform(body, validate_validate_ubl_params.ValidateValidateUblParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UblDocumentValidation,
        )


class ValidateResourceWithRawResponse:
    def __init__(self, validate: ValidateResource) -> None:
        self._validate = validate

        self.validate_json = to_raw_response_wrapper(
            validate.validate_json,
        )
        self.validate_peppol_id = to_raw_response_wrapper(
            validate.validate_peppol_id,
        )
        self.validate_ubl = to_raw_response_wrapper(
            validate.validate_ubl,
        )


class AsyncValidateResourceWithRawResponse:
    def __init__(self, validate: AsyncValidateResource) -> None:
        self._validate = validate

        self.validate_json = async_to_raw_response_wrapper(
            validate.validate_json,
        )
        self.validate_peppol_id = async_to_raw_response_wrapper(
            validate.validate_peppol_id,
        )
        self.validate_ubl = async_to_raw_response_wrapper(
            validate.validate_ubl,
        )


class ValidateResourceWithStreamingResponse:
    def __init__(self, validate: ValidateResource) -> None:
        self._validate = validate

        self.validate_json = to_streamed_response_wrapper(
            validate.validate_json,
        )
        self.validate_peppol_id = to_streamed_response_wrapper(
            validate.validate_peppol_id,
        )
        self.validate_ubl = to_streamed_response_wrapper(
            validate.validate_ubl,
        )


class AsyncValidateResourceWithStreamingResponse:
    def __init__(self, validate: AsyncValidateResource) -> None:
        self._validate = validate

        self.validate_json = async_to_streamed_response_wrapper(
            validate.validate_json,
        )
        self.validate_peppol_id = async_to_streamed_response_wrapper(
            validate.validate_peppol_id,
        )
        self.validate_ubl = async_to_streamed_response_wrapper(
            validate.validate_ubl,
        )
