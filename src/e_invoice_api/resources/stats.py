from __future__ import annotations

from typing import Union, Optional
from datetime import date
from typing_extensions import Literal

import httpx

from ..types import stats_retrieve_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
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
from ..types.stats_retrieve_response import StatsRetrieveResponse

__all__ = ["StatsResource", "AsyncStatsResource"]


class StatsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> StatsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return StatsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> StatsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return StatsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        aggregation: Optional[Literal["DAY", "WEEK", "MONTH"]] | Omit = omit,
        end_date: Union[str, date, None] | Omit = omit,
        start_date: Union[str, date, None] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StatsRetrieveResponse:
        """Retrieve usage statistics for billing purposes.

        Returns statistics for document
        sent and document received actions, grouped by aggregation period
        (day/week/month). If no date parameters are provided, returns daily stats for
        all available data.

        Args:
          aggregation: Aggregation type: DAY, WEEK, or MONTH. Defaults to DAY.

          end_date: End date in yyyy-mm-dd format. If not provided, queries to latest available
              data.

          start_date: Start date in yyyy-mm-dd format. If not provided, queries from earliest
              available data.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/stats",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "aggregation": aggregation,
                        "end_date": end_date,
                        "start_date": start_date,
                    },
                    stats_retrieve_params.StatsRetrieveParams,
                ),
            ),
            cast_to=StatsRetrieveResponse,
        )


class AsyncStatsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncStatsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return AsyncStatsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncStatsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return AsyncStatsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        aggregation: Optional[Literal["DAY", "WEEK", "MONTH"]] | Omit = omit,
        end_date: Union[str, date, None] | Omit = omit,
        start_date: Union[str, date, None] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StatsRetrieveResponse:
        """Retrieve usage statistics for billing purposes.

        Returns statistics for document
        sent and document received actions, grouped by aggregation period
        (day/week/month). If no date parameters are provided, returns daily stats for
        all available data.

        Args:
          aggregation: Aggregation type: DAY, WEEK, or MONTH. Defaults to DAY.

          end_date: End date in yyyy-mm-dd format. If not provided, queries to latest available
              data.

          start_date: Start date in yyyy-mm-dd format. If not provided, queries from earliest
              available data.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/stats",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "aggregation": aggregation,
                        "end_date": end_date,
                        "start_date": start_date,
                    },
                    stats_retrieve_params.StatsRetrieveParams,
                ),
            ),
            cast_to=StatsRetrieveResponse,
        )


class StatsResourceWithRawResponse:
    def __init__(self, stats: StatsResource) -> None:
        self._stats = stats

        self.retrieve = to_raw_response_wrapper(
            stats.retrieve,
        )


class AsyncStatsResourceWithRawResponse:
    def __init__(self, stats: AsyncStatsResource) -> None:
        self._stats = stats

        self.retrieve = async_to_raw_response_wrapper(
            stats.retrieve,
        )


class StatsResourceWithStreamingResponse:
    def __init__(self, stats: StatsResource) -> None:
        self._stats = stats

        self.retrieve = to_streamed_response_wrapper(
            stats.retrieve,
        )


class AsyncStatsResourceWithStreamingResponse:
    def __init__(self, stats: AsyncStatsResource) -> None:
        self._stats = stats

        self.retrieve = async_to_streamed_response_wrapper(
            stats.retrieve,
        )
