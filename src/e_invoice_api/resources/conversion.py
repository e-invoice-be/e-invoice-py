from __future__ import annotations

from typing import Mapping, cast

import httpx

from ..types import conversion_create_pdf_params
from .._files import deepcopy_with_paths
from .._types import Body, Query, Headers, NotGiven, FileTypes, not_given
from .._utils import extract_files, path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.conversion_pdf_task import ConversionPdfTask
from ..types.document_create_from_pdf_response import DocumentCreateFromPdfResponse

__all__ = ["ConversionResource", "AsyncConversionResource"]


class ConversionResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ConversionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return ConversionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConversionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return ConversionResourceWithStreamingResponse(self)

    def create_pdf(
        self,
        *,
        file: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ConversionPdfTask:
        """
        Convert a PDF to a document

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_with_paths({"file": file}, [["file"]])
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/api/conversion/pdf",
            body=maybe_transform(body, conversion_create_pdf_params.ConversionCreatePdfParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConversionPdfTask,
        )

    def retrieve_pdf(
        self,
        task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ConversionPdfTask:
        """
        Get the status of a PDF conversion task

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        return self._get(
            path_template("/api/conversion/pdf/{task_id}", task_id=task_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConversionPdfTask,
        )

    def retrieve_pdf_result(
        self,
        task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocumentCreateFromPdfResponse:
        """
        Get the result of a PDF conversion task

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        return self._get(
            path_template("/api/conversion/pdf/{task_id}/result", task_id=task_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentCreateFromPdfResponse,
        )


class AsyncConversionResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncConversionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return AsyncConversionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConversionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return AsyncConversionResourceWithStreamingResponse(self)

    async def create_pdf(
        self,
        *,
        file: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ConversionPdfTask:
        """
        Convert a PDF to a document

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_with_paths({"file": file}, [["file"]])
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/api/conversion/pdf",
            body=await async_maybe_transform(body, conversion_create_pdf_params.ConversionCreatePdfParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConversionPdfTask,
        )

    async def retrieve_pdf(
        self,
        task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ConversionPdfTask:
        """
        Get the status of a PDF conversion task

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        return await self._get(
            path_template("/api/conversion/pdf/{task_id}", task_id=task_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConversionPdfTask,
        )

    async def retrieve_pdf_result(
        self,
        task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocumentCreateFromPdfResponse:
        """
        Get the result of a PDF conversion task

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        return await self._get(
            path_template("/api/conversion/pdf/{task_id}/result", task_id=task_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentCreateFromPdfResponse,
        )


class ConversionResourceWithRawResponse:
    def __init__(self, conversion: ConversionResource) -> None:
        self._conversion = conversion

        self.create_pdf = to_raw_response_wrapper(
            conversion.create_pdf,
        )
        self.retrieve_pdf = to_raw_response_wrapper(
            conversion.retrieve_pdf,
        )
        self.retrieve_pdf_result = to_raw_response_wrapper(
            conversion.retrieve_pdf_result,
        )


class AsyncConversionResourceWithRawResponse:
    def __init__(self, conversion: AsyncConversionResource) -> None:
        self._conversion = conversion

        self.create_pdf = async_to_raw_response_wrapper(
            conversion.create_pdf,
        )
        self.retrieve_pdf = async_to_raw_response_wrapper(
            conversion.retrieve_pdf,
        )
        self.retrieve_pdf_result = async_to_raw_response_wrapper(
            conversion.retrieve_pdf_result,
        )


class ConversionResourceWithStreamingResponse:
    def __init__(self, conversion: ConversionResource) -> None:
        self._conversion = conversion

        self.create_pdf = to_streamed_response_wrapper(
            conversion.create_pdf,
        )
        self.retrieve_pdf = to_streamed_response_wrapper(
            conversion.retrieve_pdf,
        )
        self.retrieve_pdf_result = to_streamed_response_wrapper(
            conversion.retrieve_pdf_result,
        )


class AsyncConversionResourceWithStreamingResponse:
    def __init__(self, conversion: AsyncConversionResource) -> None:
        self._conversion = conversion

        self.create_pdf = async_to_streamed_response_wrapper(
            conversion.create_pdf,
        )
        self.retrieve_pdf = async_to_streamed_response_wrapper(
            conversion.retrieve_pdf,
        )
        self.retrieve_pdf_result = async_to_streamed_response_wrapper(
            conversion.retrieve_pdf_result,
        )
