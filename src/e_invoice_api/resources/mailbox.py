# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal

import httpx

from ..types import mailbox_list_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import path_template, maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ..pagination import SyncDocumentsNumberPage, AsyncDocumentsNumberPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.inbound_email import InboundEmail

__all__ = ["MailboxResource", "AsyncMailboxResource"]


class MailboxResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MailboxResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return MailboxResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MailboxResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return MailboxResourceWithStreamingResponse(self)

    def retrieve(
        self,
        inbound_email_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InboundEmail:
        """
        Retrieve a single inbound email by ID, scoped to the caller's tenant.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not inbound_email_id:
            raise ValueError(f"Expected a non-empty value for `inbound_email_id` but received {inbound_email_id!r}")
        return self._get(
            path_template("/api/mailbox/{inbound_email_id}", inbound_email_id=inbound_email_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InboundEmail,
        )

    def list(
        self,
        *,
        page: int | Omit = omit,
        page_size: int | Omit = omit,
        processed: Optional[bool] | Omit = omit,
        received_from: Union[str, datetime, None] | Omit = omit,
        received_to: Union[str, datetime, None] | Omit = omit,
        search: Optional[str] | Omit = omit,
        sort_by: Literal["received_at", "created_at"] | Omit = omit,
        sort_order: Literal["asc", "desc"] | Omit = omit,
        status: Optional[Literal["pending", "success", "failed"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncDocumentsNumberPage[InboundEmail]:
        """
        Retrieve a paginated list of received inbound emails with filtering, search, and
        sorting options.

        Args:
          page: Page number

          page_size: Number of items per page

          processed: Filter by processing status. If not provided, returns all. Ignored when `status`
              is set.

          received_from: Inclusive lower bound on received date (falls back to created_at when
              received_at is null)

          received_to: Inclusive upper bound on received date (falls back to created_at when
              received_at is null)

          search: Case-insensitive search across sender email, subject, message ID, and attachment
              filenames

          sort_by: Field to sort by

          sort_order: Sort direction (asc/desc)

          status: Filter by status: pending, success, or failed. Takes precedence over `processed`
              if both are provided.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/mailbox/",
            page=SyncDocumentsNumberPage[InboundEmail],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                        "processed": processed,
                        "received_from": received_from,
                        "received_to": received_to,
                        "search": search,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "status": status,
                    },
                    mailbox_list_params.MailboxListParams,
                ),
            ),
            model=InboundEmail,
        )

    def download_attachment(
        self,
        filename: str,
        *,
        inbound_email_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BinaryAPIResponse:
        """Download a specific attachment from an inbound email by filename.

        Returns the
        binary content with the correct Content-Type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not inbound_email_id:
            raise ValueError(f"Expected a non-empty value for `inbound_email_id` but received {inbound_email_id!r}")
        if not filename:
            raise ValueError(f"Expected a non-empty value for `filename` but received {filename!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            path_template(
                "/api/mailbox/{inbound_email_id}/attachments/{filename}",
                inbound_email_id=inbound_email_id,
                filename=filename,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def reprocess(
        self,
        inbound_email_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InboundEmail:
        """
        Retry processing of a previously failed inbound email by replaying the original
        Postmark payload.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not inbound_email_id:
            raise ValueError(f"Expected a non-empty value for `inbound_email_id` but received {inbound_email_id!r}")
        return self._post(
            path_template("/api/mailbox/{inbound_email_id}/reprocess", inbound_email_id=inbound_email_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InboundEmail,
        )


class AsyncMailboxResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMailboxResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return AsyncMailboxResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMailboxResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return AsyncMailboxResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        inbound_email_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InboundEmail:
        """
        Retrieve a single inbound email by ID, scoped to the caller's tenant.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not inbound_email_id:
            raise ValueError(f"Expected a non-empty value for `inbound_email_id` but received {inbound_email_id!r}")
        return await self._get(
            path_template("/api/mailbox/{inbound_email_id}", inbound_email_id=inbound_email_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InboundEmail,
        )

    def list(
        self,
        *,
        page: int | Omit = omit,
        page_size: int | Omit = omit,
        processed: Optional[bool] | Omit = omit,
        received_from: Union[str, datetime, None] | Omit = omit,
        received_to: Union[str, datetime, None] | Omit = omit,
        search: Optional[str] | Omit = omit,
        sort_by: Literal["received_at", "created_at"] | Omit = omit,
        sort_order: Literal["asc", "desc"] | Omit = omit,
        status: Optional[Literal["pending", "success", "failed"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[InboundEmail, AsyncDocumentsNumberPage[InboundEmail]]:
        """
        Retrieve a paginated list of received inbound emails with filtering, search, and
        sorting options.

        Args:
          page: Page number

          page_size: Number of items per page

          processed: Filter by processing status. If not provided, returns all. Ignored when `status`
              is set.

          received_from: Inclusive lower bound on received date (falls back to created_at when
              received_at is null)

          received_to: Inclusive upper bound on received date (falls back to created_at when
              received_at is null)

          search: Case-insensitive search across sender email, subject, message ID, and attachment
              filenames

          sort_by: Field to sort by

          sort_order: Sort direction (asc/desc)

          status: Filter by status: pending, success, or failed. Takes precedence over `processed`
              if both are provided.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/mailbox/",
            page=AsyncDocumentsNumberPage[InboundEmail],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                        "processed": processed,
                        "received_from": received_from,
                        "received_to": received_to,
                        "search": search,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "status": status,
                    },
                    mailbox_list_params.MailboxListParams,
                ),
            ),
            model=InboundEmail,
        )

    async def download_attachment(
        self,
        filename: str,
        *,
        inbound_email_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncBinaryAPIResponse:
        """Download a specific attachment from an inbound email by filename.

        Returns the
        binary content with the correct Content-Type.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not inbound_email_id:
            raise ValueError(f"Expected a non-empty value for `inbound_email_id` but received {inbound_email_id!r}")
        if not filename:
            raise ValueError(f"Expected a non-empty value for `filename` but received {filename!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            path_template(
                "/api/mailbox/{inbound_email_id}/attachments/{filename}",
                inbound_email_id=inbound_email_id,
                filename=filename,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def reprocess(
        self,
        inbound_email_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InboundEmail:
        """
        Retry processing of a previously failed inbound email by replaying the original
        Postmark payload.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not inbound_email_id:
            raise ValueError(f"Expected a non-empty value for `inbound_email_id` but received {inbound_email_id!r}")
        return await self._post(
            path_template("/api/mailbox/{inbound_email_id}/reprocess", inbound_email_id=inbound_email_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InboundEmail,
        )


class MailboxResourceWithRawResponse:
    def __init__(self, mailbox: MailboxResource) -> None:
        self._mailbox = mailbox

        self.retrieve = to_raw_response_wrapper(
            mailbox.retrieve,
        )
        self.list = to_raw_response_wrapper(
            mailbox.list,
        )
        self.download_attachment = to_custom_raw_response_wrapper(
            mailbox.download_attachment,
            BinaryAPIResponse,
        )
        self.reprocess = to_raw_response_wrapper(
            mailbox.reprocess,
        )


class AsyncMailboxResourceWithRawResponse:
    def __init__(self, mailbox: AsyncMailboxResource) -> None:
        self._mailbox = mailbox

        self.retrieve = async_to_raw_response_wrapper(
            mailbox.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            mailbox.list,
        )
        self.download_attachment = async_to_custom_raw_response_wrapper(
            mailbox.download_attachment,
            AsyncBinaryAPIResponse,
        )
        self.reprocess = async_to_raw_response_wrapper(
            mailbox.reprocess,
        )


class MailboxResourceWithStreamingResponse:
    def __init__(self, mailbox: MailboxResource) -> None:
        self._mailbox = mailbox

        self.retrieve = to_streamed_response_wrapper(
            mailbox.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            mailbox.list,
        )
        self.download_attachment = to_custom_streamed_response_wrapper(
            mailbox.download_attachment,
            StreamedBinaryAPIResponse,
        )
        self.reprocess = to_streamed_response_wrapper(
            mailbox.reprocess,
        )


class AsyncMailboxResourceWithStreamingResponse:
    def __init__(self, mailbox: AsyncMailboxResource) -> None:
        self._mailbox = mailbox

        self.retrieve = async_to_streamed_response_wrapper(
            mailbox.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            mailbox.list,
        )
        self.download_attachment = async_to_custom_streamed_response_wrapper(
            mailbox.download_attachment,
            AsyncStreamedBinaryAPIResponse,
        )
        self.reprocess = async_to_streamed_response_wrapper(
            mailbox.reprocess,
        )
