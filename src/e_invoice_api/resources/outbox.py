# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime

import httpx

from ..types import (
    DocumentType,
    DocumentState,
    outbox_list_draft_documents_params,
    outbox_list_received_documents_params,
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

__all__ = ["OutboxResource", "AsyncOutboxResource"]


class OutboxResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OutboxResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return OutboxResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OutboxResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return OutboxResourceWithStreamingResponse(self)

    def list_draft_documents(
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
        Retrieve a paginated list of draft documents with filtering options.

        Args:
          page: Page number

          page_size: Number of items per page

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/outbox/drafts",
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
                    outbox_list_draft_documents_params.OutboxListDraftDocumentsParams,
                ),
            ),
            model=DocumentResponse,
        )

    def list_received_documents(
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
            "/api/outbox/",
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
                    outbox_list_received_documents_params.OutboxListReceivedDocumentsParams,
                ),
            ),
            model=DocumentResponse,
        )


class AsyncOutboxResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOutboxResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return AsyncOutboxResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOutboxResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return AsyncOutboxResourceWithStreamingResponse(self)

    def list_draft_documents(
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
        Retrieve a paginated list of draft documents with filtering options.

        Args:
          page: Page number

          page_size: Number of items per page

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/outbox/drafts",
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
                    outbox_list_draft_documents_params.OutboxListDraftDocumentsParams,
                ),
            ),
            model=DocumentResponse,
        )

    def list_received_documents(
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
            "/api/outbox/",
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
                    outbox_list_received_documents_params.OutboxListReceivedDocumentsParams,
                ),
            ),
            model=DocumentResponse,
        )


class OutboxResourceWithRawResponse:
    def __init__(self, outbox: OutboxResource) -> None:
        self._outbox = outbox

        self.list_draft_documents = to_raw_response_wrapper(
            outbox.list_draft_documents,
        )
        self.list_received_documents = to_raw_response_wrapper(
            outbox.list_received_documents,
        )


class AsyncOutboxResourceWithRawResponse:
    def __init__(self, outbox: AsyncOutboxResource) -> None:
        self._outbox = outbox

        self.list_draft_documents = async_to_raw_response_wrapper(
            outbox.list_draft_documents,
        )
        self.list_received_documents = async_to_raw_response_wrapper(
            outbox.list_received_documents,
        )


class OutboxResourceWithStreamingResponse:
    def __init__(self, outbox: OutboxResource) -> None:
        self._outbox = outbox

        self.list_draft_documents = to_streamed_response_wrapper(
            outbox.list_draft_documents,
        )
        self.list_received_documents = to_streamed_response_wrapper(
            outbox.list_received_documents,
        )


class AsyncOutboxResourceWithStreamingResponse:
    def __init__(self, outbox: AsyncOutboxResource) -> None:
        self._outbox = outbox

        self.list_draft_documents = async_to_streamed_response_wrapper(
            outbox.list_draft_documents,
        )
        self.list_received_documents = async_to_streamed_response_wrapper(
            outbox.list_received_documents,
        )
