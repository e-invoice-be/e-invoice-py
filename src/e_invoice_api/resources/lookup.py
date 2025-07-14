# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import lookup_retrieve_params, lookup_retrieve_participants_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.lookup_retrieve_response import LookupRetrieveResponse
from ..types.lookup_retrieve_participants_response import LookupRetrieveParticipantsResponse

__all__ = ["LookupResource", "AsyncLookupResource"]


class LookupResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> LookupResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return LookupResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LookupResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return LookupResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        peppol_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LookupRetrieveResponse:
        """Lookup Peppol ID.

        The peppol_id must be in the form of `<scheme>:<id>`. The
        scheme is a 4-digit code representing the identifier scheme, and the id is the
        actual identifier value. For example, for a Belgian company it is
        `0208:0123456789` (where 0208 is the scheme for Belgian enterprises, followed by
        the 10 digits of the official BTW / KBO number).

        Args:
          peppol_id: Peppol ID in the format `<scheme>:<id>`. Example: `0208:1018265814` for a
              Belgian company.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/lookup",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"peppol_id": peppol_id}, lookup_retrieve_params.LookupRetrieveParams),
            ),
            cast_to=LookupRetrieveResponse,
        )

    def retrieve_participants(
        self,
        *,
        query: str,
        country_code: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LookupRetrieveParticipantsResponse:
        """Lookup Peppol participants by name or other identifiers.

        You can limit the
        search to a specific country by providing the country code.

        Args:
          query: Query to lookup

          country_code: Country code of the company to lookup. If not provided, the search will be
              global.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/lookup/participants",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "query": query,
                        "country_code": country_code,
                    },
                    lookup_retrieve_participants_params.LookupRetrieveParticipantsParams,
                ),
            ),
            cast_to=LookupRetrieveParticipantsResponse,
        )


class AsyncLookupResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncLookupResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return AsyncLookupResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLookupResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return AsyncLookupResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        peppol_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LookupRetrieveResponse:
        """Lookup Peppol ID.

        The peppol_id must be in the form of `<scheme>:<id>`. The
        scheme is a 4-digit code representing the identifier scheme, and the id is the
        actual identifier value. For example, for a Belgian company it is
        `0208:0123456789` (where 0208 is the scheme for Belgian enterprises, followed by
        the 10 digits of the official BTW / KBO number).

        Args:
          peppol_id: Peppol ID in the format `<scheme>:<id>`. Example: `0208:1018265814` for a
              Belgian company.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/lookup",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"peppol_id": peppol_id}, lookup_retrieve_params.LookupRetrieveParams
                ),
            ),
            cast_to=LookupRetrieveResponse,
        )

    async def retrieve_participants(
        self,
        *,
        query: str,
        country_code: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LookupRetrieveParticipantsResponse:
        """Lookup Peppol participants by name or other identifiers.

        You can limit the
        search to a specific country by providing the country code.

        Args:
          query: Query to lookup

          country_code: Country code of the company to lookup. If not provided, the search will be
              global.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/lookup/participants",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "query": query,
                        "country_code": country_code,
                    },
                    lookup_retrieve_participants_params.LookupRetrieveParticipantsParams,
                ),
            ),
            cast_to=LookupRetrieveParticipantsResponse,
        )


class LookupResourceWithRawResponse:
    def __init__(self, lookup: LookupResource) -> None:
        self._lookup = lookup

        self.retrieve = to_raw_response_wrapper(
            lookup.retrieve,
        )
        self.retrieve_participants = to_raw_response_wrapper(
            lookup.retrieve_participants,
        )


class AsyncLookupResourceWithRawResponse:
    def __init__(self, lookup: AsyncLookupResource) -> None:
        self._lookup = lookup

        self.retrieve = async_to_raw_response_wrapper(
            lookup.retrieve,
        )
        self.retrieve_participants = async_to_raw_response_wrapper(
            lookup.retrieve_participants,
        )


class LookupResourceWithStreamingResponse:
    def __init__(self, lookup: LookupResource) -> None:
        self._lookup = lookup

        self.retrieve = to_streamed_response_wrapper(
            lookup.retrieve,
        )
        self.retrieve_participants = to_streamed_response_wrapper(
            lookup.retrieve_participants,
        )


class AsyncLookupResourceWithStreamingResponse:
    def __init__(self, lookup: AsyncLookupResource) -> None:
        self._lookup = lookup

        self.retrieve = async_to_streamed_response_wrapper(
            lookup.retrieve,
        )
        self.retrieve_participants = async_to_streamed_response_wrapper(
            lookup.retrieve_participants,
        )
