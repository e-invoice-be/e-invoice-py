# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from datetime import date
from typing_extensions import Literal

import httpx

from .ubl import (
    UblResource,
    AsyncUblResource,
    UblResourceWithRawResponse,
    AsyncUblResourceWithRawResponse,
    UblResourceWithStreamingResponse,
    AsyncUblResourceWithStreamingResponse,
)
from ...types import (
    CurrencyCode,
    DocumentType,
    DocumentState,
    DocumentDirection,
    document_send_params,
    document_create_params,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .attachments import (
    AttachmentsResource,
    AsyncAttachmentsResource,
    AttachmentsResourceWithRawResponse,
    AsyncAttachmentsResourceWithRawResponse,
    AttachmentsResourceWithStreamingResponse,
    AsyncAttachmentsResourceWithStreamingResponse,
)
from ..._base_client import make_request_options
from ...types.currency_code import CurrencyCode
from ...types.document_type import DocumentType
from ...types.document_state import DocumentState
from ...types.document_response import DocumentResponse
from ...types.document_direction import DocumentDirection
from ...types.document_delete_response import DocumentDeleteResponse
from ...types.payment_detail_create_param import PaymentDetailCreateParam
from ...types.document_attachment_create_param import DocumentAttachmentCreateParam

__all__ = ["DocumentsResource", "AsyncDocumentsResource"]


class DocumentsResource(SyncAPIResource):
    @cached_property
    def attachments(self) -> AttachmentsResource:
        return AttachmentsResource(self._client)

    @cached_property
    def ubl(self) -> UblResource:
        return UblResource(self._client)

    @cached_property
    def with_raw_response(self) -> DocumentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return DocumentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DocumentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return DocumentsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        amount_due: Union[float, str, None] | Omit = omit,
        attachments: Optional[Iterable[DocumentAttachmentCreateParam]] | Omit = omit,
        billing_address: Optional[str] | Omit = omit,
        billing_address_recipient: Optional[str] | Omit = omit,
        currency: CurrencyCode | Omit = omit,
        customer_address: Optional[str] | Omit = omit,
        customer_address_recipient: Optional[str] | Omit = omit,
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
        items: Optional[Iterable[document_create_params.Item]] | Omit = omit,
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
        tax_details: Optional[Iterable[document_create_params.TaxDetail]] | Omit = omit,
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
        vendor_email: Optional[str] | Omit = omit,
        vendor_name: Optional[str] | Omit = omit,
        vendor_tax_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocumentResponse:
        """
        Create a new invoice or credit note

        Args:
          currency: Currency of the invoice

          tax_code: Tax category code of the invoice

          vatex: VATEX code list for VAT exemption reasons

              Agency: CEF Identifier: vatex

          vatex_note: VAT exemption note of the invoice

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/documents/",
            body=maybe_transform(
                {
                    "amount_due": amount_due,
                    "attachments": attachments,
                    "billing_address": billing_address,
                    "billing_address_recipient": billing_address_recipient,
                    "currency": currency,
                    "customer_address": customer_address,
                    "customer_address_recipient": customer_address_recipient,
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
                    "vendor_email": vendor_email,
                    "vendor_name": vendor_name,
                    "vendor_tax_id": vendor_tax_id,
                },
                document_create_params.DocumentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentResponse,
        )

    def retrieve(
        self,
        document_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocumentResponse:
        """
        Get an invoice or credit note by ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return self._get(
            f"/api/documents/{document_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentResponse,
        )

    def delete(
        self,
        document_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocumentDeleteResponse:
        """
        Delete an invoice or credit note

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return self._delete(
            f"/api/documents/{document_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentDeleteResponse,
        )

    def send(
        self,
        document_id: str,
        *,
        email: Optional[str] | Omit = omit,
        receiver_peppol_id: Optional[str] | Omit = omit,
        receiver_peppol_scheme: Optional[str] | Omit = omit,
        sender_peppol_id: Optional[str] | Omit = omit,
        sender_peppol_scheme: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocumentResponse:
        """
        Send an invoice or credit note via Peppol

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return self._post(
            f"/api/documents/{document_id}/send",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "email": email,
                        "receiver_peppol_id": receiver_peppol_id,
                        "receiver_peppol_scheme": receiver_peppol_scheme,
                        "sender_peppol_id": sender_peppol_id,
                        "sender_peppol_scheme": sender_peppol_scheme,
                    },
                    document_send_params.DocumentSendParams,
                ),
            ),
            cast_to=DocumentResponse,
        )


class AsyncDocumentsResource(AsyncAPIResource):
    @cached_property
    def attachments(self) -> AsyncAttachmentsResource:
        return AsyncAttachmentsResource(self._client)

    @cached_property
    def ubl(self) -> AsyncUblResource:
        return AsyncUblResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDocumentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return AsyncDocumentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDocumentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return AsyncDocumentsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        amount_due: Union[float, str, None] | Omit = omit,
        attachments: Optional[Iterable[DocumentAttachmentCreateParam]] | Omit = omit,
        billing_address: Optional[str] | Omit = omit,
        billing_address_recipient: Optional[str] | Omit = omit,
        currency: CurrencyCode | Omit = omit,
        customer_address: Optional[str] | Omit = omit,
        customer_address_recipient: Optional[str] | Omit = omit,
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
        items: Optional[Iterable[document_create_params.Item]] | Omit = omit,
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
        tax_details: Optional[Iterable[document_create_params.TaxDetail]] | Omit = omit,
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
        vendor_email: Optional[str] | Omit = omit,
        vendor_name: Optional[str] | Omit = omit,
        vendor_tax_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocumentResponse:
        """
        Create a new invoice or credit note

        Args:
          currency: Currency of the invoice

          tax_code: Tax category code of the invoice

          vatex: VATEX code list for VAT exemption reasons

              Agency: CEF Identifier: vatex

          vatex_note: VAT exemption note of the invoice

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/documents/",
            body=await async_maybe_transform(
                {
                    "amount_due": amount_due,
                    "attachments": attachments,
                    "billing_address": billing_address,
                    "billing_address_recipient": billing_address_recipient,
                    "currency": currency,
                    "customer_address": customer_address,
                    "customer_address_recipient": customer_address_recipient,
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
                    "vendor_email": vendor_email,
                    "vendor_name": vendor_name,
                    "vendor_tax_id": vendor_tax_id,
                },
                document_create_params.DocumentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentResponse,
        )

    async def retrieve(
        self,
        document_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocumentResponse:
        """
        Get an invoice or credit note by ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return await self._get(
            f"/api/documents/{document_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentResponse,
        )

    async def delete(
        self,
        document_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocumentDeleteResponse:
        """
        Delete an invoice or credit note

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return await self._delete(
            f"/api/documents/{document_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentDeleteResponse,
        )

    async def send(
        self,
        document_id: str,
        *,
        email: Optional[str] | Omit = omit,
        receiver_peppol_id: Optional[str] | Omit = omit,
        receiver_peppol_scheme: Optional[str] | Omit = omit,
        sender_peppol_id: Optional[str] | Omit = omit,
        sender_peppol_scheme: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocumentResponse:
        """
        Send an invoice or credit note via Peppol

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return await self._post(
            f"/api/documents/{document_id}/send",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "email": email,
                        "receiver_peppol_id": receiver_peppol_id,
                        "receiver_peppol_scheme": receiver_peppol_scheme,
                        "sender_peppol_id": sender_peppol_id,
                        "sender_peppol_scheme": sender_peppol_scheme,
                    },
                    document_send_params.DocumentSendParams,
                ),
            ),
            cast_to=DocumentResponse,
        )


class DocumentsResourceWithRawResponse:
    def __init__(self, documents: DocumentsResource) -> None:
        self._documents = documents

        self.create = to_raw_response_wrapper(
            documents.create,
        )
        self.retrieve = to_raw_response_wrapper(
            documents.retrieve,
        )
        self.delete = to_raw_response_wrapper(
            documents.delete,
        )
        self.send = to_raw_response_wrapper(
            documents.send,
        )

    @cached_property
    def attachments(self) -> AttachmentsResourceWithRawResponse:
        return AttachmentsResourceWithRawResponse(self._documents.attachments)

    @cached_property
    def ubl(self) -> UblResourceWithRawResponse:
        return UblResourceWithRawResponse(self._documents.ubl)


class AsyncDocumentsResourceWithRawResponse:
    def __init__(self, documents: AsyncDocumentsResource) -> None:
        self._documents = documents

        self.create = async_to_raw_response_wrapper(
            documents.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            documents.retrieve,
        )
        self.delete = async_to_raw_response_wrapper(
            documents.delete,
        )
        self.send = async_to_raw_response_wrapper(
            documents.send,
        )

    @cached_property
    def attachments(self) -> AsyncAttachmentsResourceWithRawResponse:
        return AsyncAttachmentsResourceWithRawResponse(self._documents.attachments)

    @cached_property
    def ubl(self) -> AsyncUblResourceWithRawResponse:
        return AsyncUblResourceWithRawResponse(self._documents.ubl)


class DocumentsResourceWithStreamingResponse:
    def __init__(self, documents: DocumentsResource) -> None:
        self._documents = documents

        self.create = to_streamed_response_wrapper(
            documents.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            documents.retrieve,
        )
        self.delete = to_streamed_response_wrapper(
            documents.delete,
        )
        self.send = to_streamed_response_wrapper(
            documents.send,
        )

    @cached_property
    def attachments(self) -> AttachmentsResourceWithStreamingResponse:
        return AttachmentsResourceWithStreamingResponse(self._documents.attachments)

    @cached_property
    def ubl(self) -> UblResourceWithStreamingResponse:
        return UblResourceWithStreamingResponse(self._documents.ubl)


class AsyncDocumentsResourceWithStreamingResponse:
    def __init__(self, documents: AsyncDocumentsResource) -> None:
        self._documents = documents

        self.create = async_to_streamed_response_wrapper(
            documents.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            documents.retrieve,
        )
        self.delete = async_to_streamed_response_wrapper(
            documents.delete,
        )
        self.send = async_to_streamed_response_wrapper(
            documents.send,
        )

    @cached_property
    def attachments(self) -> AsyncAttachmentsResourceWithStreamingResponse:
        return AsyncAttachmentsResourceWithStreamingResponse(self._documents.attachments)

    @cached_property
    def ubl(self) -> AsyncUblResourceWithStreamingResponse:
        return AsyncUblResourceWithStreamingResponse(self._documents.ubl)
