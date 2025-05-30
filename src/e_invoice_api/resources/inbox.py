# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime

import httpx

from ..types import (
    DocumentType,
    DocumentState,
    inbox_list_params,
    inbox_list_invoices_params,
    inbox_list_credit_notes_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncDocumentsNumberPage, AsyncDocumentsNumberPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.document_type import DocumentType
from ..types.document_state import DocumentState
from ..types.document_response import DocumentResponse

__all__ = ["InboxResource", "AsyncInboxResource"]


class InboxResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> InboxResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return InboxResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InboxResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return InboxResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        date_from: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        date_to: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        search: Optional[str] | NotGiven = NOT_GIVEN,
        sender: Optional[str] | NotGiven = NOT_GIVEN,
        state: Optional[DocumentState] | NotGiven = NOT_GIVEN,
        type: Optional[DocumentType] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncDocumentsNumberPage[DocumentResponse]:
        """
        Retrieve a paginated list of received documents with filtering options.

        Args:
          date_from: Filter by issue date (from)

          date_to: Filter by issue date (to)

          page: Page number

          page_size: Number of items per page

          search: Search in invoice number, seller/buyer names

          sender: Filter by sender ID

          state: Filter by document state

          type: Filter by document type

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/inbox/",
            page=SyncDocumentsNumberPage[DocumentResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "date_from": date_from,
                        "date_to": date_to,
                        "page": page,
                        "page_size": page_size,
                        "search": search,
                        "sender": sender,
                        "state": state,
                        "type": type,
                    },
                    inbox_list_params.InboxListParams,
                ),
            ),
            model=DocumentResponse,
        )

    def list_credit_notes(
        self,
        *,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncDocumentsNumberPage[DocumentResponse]:
        """
        Retrieve a paginated list of received credit notes with filtering options.

        Args:
          page: Page number

          page_size: Number of items per page

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/inbox/credit-notes",
            page=SyncDocumentsNumberPage[DocumentResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                    },
                    inbox_list_credit_notes_params.InboxListCreditNotesParams,
                ),
            ),
            model=DocumentResponse,
        )

    def list_invoices(
        self,
        *,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncDocumentsNumberPage[DocumentResponse]:
        """
        Retrieve a paginated list of received invoices with filtering options.

        Args:
          page: Page number

          page_size: Number of items per page

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/inbox/invoices",
            page=SyncDocumentsNumberPage[DocumentResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                    },
                    inbox_list_invoices_params.InboxListInvoicesParams,
                ),
            ),
            model=DocumentResponse,
        )


class AsyncInboxResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncInboxResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return AsyncInboxResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInboxResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return AsyncInboxResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        date_from: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        date_to: Union[str, datetime, None] | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        search: Optional[str] | NotGiven = NOT_GIVEN,
        sender: Optional[str] | NotGiven = NOT_GIVEN,
        state: Optional[DocumentState] | NotGiven = NOT_GIVEN,
        type: Optional[DocumentType] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[DocumentResponse, AsyncDocumentsNumberPage[DocumentResponse]]:
        """
        Retrieve a paginated list of received documents with filtering options.

        Args:
          date_from: Filter by issue date (from)

          date_to: Filter by issue date (to)

          page: Page number

          page_size: Number of items per page

          search: Search in invoice number, seller/buyer names

          sender: Filter by sender ID

          state: Filter by document state

          type: Filter by document type

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/inbox/",
            page=AsyncDocumentsNumberPage[DocumentResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "date_from": date_from,
                        "date_to": date_to,
                        "page": page,
                        "page_size": page_size,
                        "search": search,
                        "sender": sender,
                        "state": state,
                        "type": type,
                    },
                    inbox_list_params.InboxListParams,
                ),
            ),
            model=DocumentResponse,
        )

    def list_credit_notes(
        self,
        *,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[DocumentResponse, AsyncDocumentsNumberPage[DocumentResponse]]:
        """
        Retrieve a paginated list of received credit notes with filtering options.

        Args:
          page: Page number

          page_size: Number of items per page

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/inbox/credit-notes",
            page=AsyncDocumentsNumberPage[DocumentResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                    },
                    inbox_list_credit_notes_params.InboxListCreditNotesParams,
                ),
            ),
            model=DocumentResponse,
        )

    def list_invoices(
        self,
        *,
        page: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[DocumentResponse, AsyncDocumentsNumberPage[DocumentResponse]]:
        """
        Retrieve a paginated list of received invoices with filtering options.

        Args:
          page: Page number

          page_size: Number of items per page

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/inbox/invoices",
            page=AsyncDocumentsNumberPage[DocumentResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                    },
                    inbox_list_invoices_params.InboxListInvoicesParams,
                ),
            ),
            model=DocumentResponse,
        )


class InboxResourceWithRawResponse:
    def __init__(self, inbox: InboxResource) -> None:
        self._inbox = inbox

        self.list = to_raw_response_wrapper(
            inbox.list,
        )
        self.list_credit_notes = to_raw_response_wrapper(
            inbox.list_credit_notes,
        )
        self.list_invoices = to_raw_response_wrapper(
            inbox.list_invoices,
        )


class AsyncInboxResourceWithRawResponse:
    def __init__(self, inbox: AsyncInboxResource) -> None:
        self._inbox = inbox

        self.list = async_to_raw_response_wrapper(
            inbox.list,
        )
        self.list_credit_notes = async_to_raw_response_wrapper(
            inbox.list_credit_notes,
        )
        self.list_invoices = async_to_raw_response_wrapper(
            inbox.list_invoices,
        )


class InboxResourceWithStreamingResponse:
    def __init__(self, inbox: InboxResource) -> None:
        self._inbox = inbox

        self.list = to_streamed_response_wrapper(
            inbox.list,
        )
        self.list_credit_notes = to_streamed_response_wrapper(
            inbox.list_credit_notes,
        )
        self.list_invoices = to_streamed_response_wrapper(
            inbox.list_invoices,
        )


class AsyncInboxResourceWithStreamingResponse:
    def __init__(self, inbox: AsyncInboxResource) -> None:
        self._inbox = inbox

        self.list = async_to_streamed_response_wrapper(
            inbox.list,
        )
        self.list_credit_notes = async_to_streamed_response_wrapper(
            inbox.list_credit_notes,
        )
        self.list_invoices = async_to_streamed_response_wrapper(
            inbox.list_invoices,
        )
