# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from datetime import date

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
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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
        amount_due: Union[float, str, None] | NotGiven = NOT_GIVEN,
        attachments: Optional[Iterable[DocumentAttachmentCreateParam]] | NotGiven = NOT_GIVEN,
        billing_address: Optional[str] | NotGiven = NOT_GIVEN,
        billing_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        currency: CurrencyCode | NotGiven = NOT_GIVEN,
        customer_address: Optional[str] | NotGiven = NOT_GIVEN,
        customer_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        customer_email: Optional[str] | NotGiven = NOT_GIVEN,
        customer_id: Optional[str] | NotGiven = NOT_GIVEN,
        customer_name: Optional[str] | NotGiven = NOT_GIVEN,
        customer_tax_id: Optional[str] | NotGiven = NOT_GIVEN,
        direction: DocumentDirection | NotGiven = NOT_GIVEN,
        document_type: DocumentType | NotGiven = NOT_GIVEN,
        due_date: Union[str, date, None] | NotGiven = NOT_GIVEN,
        invoice_date: Union[str, date, None] | NotGiven = NOT_GIVEN,
        invoice_id: Optional[str] | NotGiven = NOT_GIVEN,
        invoice_total: Union[float, str, None] | NotGiven = NOT_GIVEN,
        items: Optional[Iterable[document_create_params.Item]] | NotGiven = NOT_GIVEN,
        note: Optional[str] | NotGiven = NOT_GIVEN,
        payment_details: Optional[Iterable[PaymentDetailCreateParam]] | NotGiven = NOT_GIVEN,
        payment_term: Optional[str] | NotGiven = NOT_GIVEN,
        previous_unpaid_balance: Union[float, str, None] | NotGiven = NOT_GIVEN,
        purchase_order: Optional[str] | NotGiven = NOT_GIVEN,
        remittance_address: Optional[str] | NotGiven = NOT_GIVEN,
        remittance_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        service_address: Optional[str] | NotGiven = NOT_GIVEN,
        service_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        service_end_date: Union[str, date, None] | NotGiven = NOT_GIVEN,
        service_start_date: Union[str, date, None] | NotGiven = NOT_GIVEN,
        shipping_address: Optional[str] | NotGiven = NOT_GIVEN,
        shipping_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        state: DocumentState | NotGiven = NOT_GIVEN,
        subtotal: Union[float, str, None] | NotGiven = NOT_GIVEN,
        tax_details: Optional[Iterable[document_create_params.TaxDetail]] | NotGiven = NOT_GIVEN,
        total_discount: Union[float, str, None] | NotGiven = NOT_GIVEN,
        total_tax: Union[float, str, None] | NotGiven = NOT_GIVEN,
        vendor_address: Optional[str] | NotGiven = NOT_GIVEN,
        vendor_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        vendor_email: Optional[str] | NotGiven = NOT_GIVEN,
        vendor_name: Optional[str] | NotGiven = NOT_GIVEN,
        vendor_tax_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentResponse:
        """
        Create a new invoice or credit note

        Args:
          currency: Currency of the invoice

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
                    "tax_details": tax_details,
                    "total_discount": total_discount,
                    "total_tax": total_tax,
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
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
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
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
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
        email: Optional[str] | NotGiven = NOT_GIVEN,
        receiver_peppol_id: Optional[str] | NotGiven = NOT_GIVEN,
        receiver_peppol_scheme: Optional[str] | NotGiven = NOT_GIVEN,
        sender_peppol_id: Optional[str] | NotGiven = NOT_GIVEN,
        sender_peppol_scheme: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
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
        amount_due: Union[float, str, None] | NotGiven = NOT_GIVEN,
        attachments: Optional[Iterable[DocumentAttachmentCreateParam]] | NotGiven = NOT_GIVEN,
        billing_address: Optional[str] | NotGiven = NOT_GIVEN,
        billing_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        currency: CurrencyCode | NotGiven = NOT_GIVEN,
        customer_address: Optional[str] | NotGiven = NOT_GIVEN,
        customer_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        customer_email: Optional[str] | NotGiven = NOT_GIVEN,
        customer_id: Optional[str] | NotGiven = NOT_GIVEN,
        customer_name: Optional[str] | NotGiven = NOT_GIVEN,
        customer_tax_id: Optional[str] | NotGiven = NOT_GIVEN,
        direction: DocumentDirection | NotGiven = NOT_GIVEN,
        document_type: DocumentType | NotGiven = NOT_GIVEN,
        due_date: Union[str, date, None] | NotGiven = NOT_GIVEN,
        invoice_date: Union[str, date, None] | NotGiven = NOT_GIVEN,
        invoice_id: Optional[str] | NotGiven = NOT_GIVEN,
        invoice_total: Union[float, str, None] | NotGiven = NOT_GIVEN,
        items: Optional[Iterable[document_create_params.Item]] | NotGiven = NOT_GIVEN,
        note: Optional[str] | NotGiven = NOT_GIVEN,
        payment_details: Optional[Iterable[PaymentDetailCreateParam]] | NotGiven = NOT_GIVEN,
        payment_term: Optional[str] | NotGiven = NOT_GIVEN,
        previous_unpaid_balance: Union[float, str, None] | NotGiven = NOT_GIVEN,
        purchase_order: Optional[str] | NotGiven = NOT_GIVEN,
        remittance_address: Optional[str] | NotGiven = NOT_GIVEN,
        remittance_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        service_address: Optional[str] | NotGiven = NOT_GIVEN,
        service_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        service_end_date: Union[str, date, None] | NotGiven = NOT_GIVEN,
        service_start_date: Union[str, date, None] | NotGiven = NOT_GIVEN,
        shipping_address: Optional[str] | NotGiven = NOT_GIVEN,
        shipping_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        state: DocumentState | NotGiven = NOT_GIVEN,
        subtotal: Union[float, str, None] | NotGiven = NOT_GIVEN,
        tax_details: Optional[Iterable[document_create_params.TaxDetail]] | NotGiven = NOT_GIVEN,
        total_discount: Union[float, str, None] | NotGiven = NOT_GIVEN,
        total_tax: Union[float, str, None] | NotGiven = NOT_GIVEN,
        vendor_address: Optional[str] | NotGiven = NOT_GIVEN,
        vendor_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        vendor_email: Optional[str] | NotGiven = NOT_GIVEN,
        vendor_name: Optional[str] | NotGiven = NOT_GIVEN,
        vendor_tax_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentResponse:
        """
        Create a new invoice or credit note

        Args:
          currency: Currency of the invoice

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
                    "tax_details": tax_details,
                    "total_discount": total_discount,
                    "total_tax": total_tax,
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
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
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
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
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
        email: Optional[str] | NotGiven = NOT_GIVEN,
        receiver_peppol_id: Optional[str] | NotGiven = NOT_GIVEN,
        receiver_peppol_scheme: Optional[str] | NotGiven = NOT_GIVEN,
        sender_peppol_id: Optional[str] | NotGiven = NOT_GIVEN,
        sender_peppol_scheme: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
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
