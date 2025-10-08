# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Mapping, cast

import httpx

from ..._types import Body, Query, Headers, NotGiven, FileTypes, not_given
from ..._utils import extract_files, maybe_transform, deepcopy_minimal, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.documents import ubl_create_from_ubl_params
from ...types.document_response import DocumentResponse
from ...types.documents.ubl_get_response import UblGetResponse

__all__ = ["UblResource", "AsyncUblResource"]


class UblResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UblResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return UblResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UblResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return UblResourceWithStreamingResponse(self)

    def create_from_ubl(
        self,
        *,
        file: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocumentResponse:
        """
        Create a new invoice or credit note from a UBL file

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
            "/api/documents/ubl",
            body=maybe_transform(body, ubl_create_from_ubl_params.UblCreateFromUblParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentResponse,
        )

    def get(
        self,
        document_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UblGetResponse:
        """
        Get the UBL for an invoice or credit note

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return self._get(
            f"/api/documents/{document_id}/ubl",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UblGetResponse,
        )


class AsyncUblResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUblResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return AsyncUblResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUblResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return AsyncUblResourceWithStreamingResponse(self)

    async def create_from_ubl(
        self,
        *,
        file: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocumentResponse:
        """
        Create a new invoice or credit note from a UBL file

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
            "/api/documents/ubl",
            body=await async_maybe_transform(body, ubl_create_from_ubl_params.UblCreateFromUblParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentResponse,
        )

    async def get(
        self,
        document_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> UblGetResponse:
        """
        Get the UBL for an invoice or credit note

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return await self._get(
            f"/api/documents/{document_id}/ubl",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UblGetResponse,
        )


class UblResourceWithRawResponse:
    def __init__(self, ubl: UblResource) -> None:
        self._ubl = ubl

        self.create_from_ubl = to_raw_response_wrapper(
            ubl.create_from_ubl,
        )
        self.get = to_raw_response_wrapper(
            ubl.get,
        )


class AsyncUblResourceWithRawResponse:
    def __init__(self, ubl: AsyncUblResource) -> None:
        self._ubl = ubl

        self.create_from_ubl = async_to_raw_response_wrapper(
            ubl.create_from_ubl,
        )
        self.get = async_to_raw_response_wrapper(
            ubl.get,
        )


class UblResourceWithStreamingResponse:
    def __init__(self, ubl: UblResource) -> None:
        self._ubl = ubl

        self.create_from_ubl = to_streamed_response_wrapper(
            ubl.create_from_ubl,
        )
        self.get = to_streamed_response_wrapper(
            ubl.get,
        )


class AsyncUblResourceWithStreamingResponse:
    def __init__(self, ubl: AsyncUblResource) -> None:
        self._ubl = ubl

        self.create_from_ubl = async_to_streamed_response_wrapper(
            ubl.create_from_ubl,
        )
        self.get = async_to_streamed_response_wrapper(
            ubl.get,
        )
