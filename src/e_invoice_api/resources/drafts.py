from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal

import httpx

from ..types import DocumentType, DocumentState, draft_list_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
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

__all__ = ["DraftsResource", "AsyncDraftsResource"]


class DraftsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DraftsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return DraftsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DraftsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return DraftsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        date_from: Union[str, datetime, None] | Omit = omit,
        date_to: Union[str, datetime, None] | Omit = omit,
        page: int | Omit = omit,
        page_size: int | Omit = omit,
        search: Optional[str] | Omit = omit,
        sort_by: Literal[
            "created_at", "invoice_date", "due_date", "invoice_total", "customer_name", "vendor_name", "invoice_id"
        ]
        | Omit = omit,
        sort_order: Literal["asc", "desc"] | Omit = omit,
        state: Optional[DocumentState] | Omit = omit,
        type: Optional[DocumentType] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncDocumentsNumberPage[DocumentResponse]:
        """
        Retrieve a paginated list of draft documents with filtering options including
        state and text search.

        Args:
          date_from: Filter by issue date (from)

          date_to: Filter by issue date (to)

          page: Page number

          page_size: Number of items per page

          search: Search in invoice number, seller/buyer names

          sort_by: Field to sort by

          sort_order: Sort direction (asc/desc)

          state: Filter by document state. By default return all states (DRAFT, TRANSIT, FAILED).

          type: Filter by document type

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/drafts/",
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
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "state": state,
                        "type": type,
                    },
                    draft_list_params.DraftListParams,
                ),
            ),
            model=DocumentResponse,
        )


class AsyncDraftsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDraftsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return AsyncDraftsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDraftsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return AsyncDraftsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        date_from: Union[str, datetime, None] | Omit = omit,
        date_to: Union[str, datetime, None] | Omit = omit,
        page: int | Omit = omit,
        page_size: int | Omit = omit,
        search: Optional[str] | Omit = omit,
        sort_by: Literal[
            "created_at", "invoice_date", "due_date", "invoice_total", "customer_name", "vendor_name", "invoice_id"
        ]
        | Omit = omit,
        sort_order: Literal["asc", "desc"] | Omit = omit,
        state: Optional[DocumentState] | Omit = omit,
        type: Optional[DocumentType] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[DocumentResponse, AsyncDocumentsNumberPage[DocumentResponse]]:
        """
        Retrieve a paginated list of draft documents with filtering options including
        state and text search.

        Args:
          date_from: Filter by issue date (from)

          date_to: Filter by issue date (to)

          page: Page number

          page_size: Number of items per page

          search: Search in invoice number, seller/buyer names

          sort_by: Field to sort by

          sort_order: Sort direction (asc/desc)

          state: Filter by document state. By default return all states (DRAFT, TRANSIT, FAILED).

          type: Filter by document type

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/drafts/",
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
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "state": state,
                        "type": type,
                    },
                    draft_list_params.DraftListParams,
                ),
            ),
            model=DocumentResponse,
        )


class DraftsResourceWithRawResponse:
    def __init__(self, drafts: DraftsResource) -> None:
        self._drafts = drafts

        self.list = to_raw_response_wrapper(
            drafts.list,
        )


class AsyncDraftsResourceWithRawResponse:
    def __init__(self, drafts: AsyncDraftsResource) -> None:
        self._drafts = drafts

        self.list = async_to_raw_response_wrapper(
            drafts.list,
        )


class DraftsResourceWithStreamingResponse:
    def __init__(self, drafts: DraftsResource) -> None:
        self._drafts = drafts

        self.list = to_streamed_response_wrapper(
            drafts.list,
        )


class AsyncDraftsResourceWithStreamingResponse:
    def __init__(self, drafts: AsyncDraftsResource) -> None:
        self._drafts = drafts

        self.list = async_to_streamed_response_wrapper(
            drafts.list,
        )
