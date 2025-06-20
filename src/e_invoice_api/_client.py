# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from .resources import inbox, lookup, outbox, validate, webhooks
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import EInvoiceError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)
from .resources.documents import documents

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "EInvoice",
    "AsyncEInvoice",
    "Client",
    "AsyncClient",
]


class EInvoice(SyncAPIClient):
    documents: documents.DocumentsResource
    inbox: inbox.InboxResource
    outbox: outbox.OutboxResource
    validate: validate.ValidateResource
    lookup: lookup.LookupResource
    webhooks: webhooks.WebhooksResource
    with_raw_response: EInvoiceWithRawResponse
    with_streaming_response: EInvoiceWithStreamedResponse

    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous EInvoice client instance.

        This automatically infers the `api_key` argument from the `E_INVOICE_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("E_INVOICE_API_KEY")
        if api_key is None:
            raise EInvoiceError(
                "The api_key client option must be set either by passing api_key to the client or by setting the E_INVOICE_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("E_INVOICE_BASE_URL")
        if base_url is None:
            base_url = f"https://api.e-invoice.be"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.documents = documents.DocumentsResource(self)
        self.inbox = inbox.InboxResource(self)
        self.outbox = outbox.OutboxResource(self)
        self.validate = validate.ValidateResource(self)
        self.lookup = lookup.LookupResource(self)
        self.webhooks = webhooks.WebhooksResource(self)
        self.with_raw_response = EInvoiceWithRawResponse(self)
        self.with_streaming_response = EInvoiceWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncEInvoice(AsyncAPIClient):
    documents: documents.AsyncDocumentsResource
    inbox: inbox.AsyncInboxResource
    outbox: outbox.AsyncOutboxResource
    validate: validate.AsyncValidateResource
    lookup: lookup.AsyncLookupResource
    webhooks: webhooks.AsyncWebhooksResource
    with_raw_response: AsyncEInvoiceWithRawResponse
    with_streaming_response: AsyncEInvoiceWithStreamedResponse

    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncEInvoice client instance.

        This automatically infers the `api_key` argument from the `E_INVOICE_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("E_INVOICE_API_KEY")
        if api_key is None:
            raise EInvoiceError(
                "The api_key client option must be set either by passing api_key to the client or by setting the E_INVOICE_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("E_INVOICE_BASE_URL")
        if base_url is None:
            base_url = f"https://api.e-invoice.be"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.documents = documents.AsyncDocumentsResource(self)
        self.inbox = inbox.AsyncInboxResource(self)
        self.outbox = outbox.AsyncOutboxResource(self)
        self.validate = validate.AsyncValidateResource(self)
        self.lookup = lookup.AsyncLookupResource(self)
        self.webhooks = webhooks.AsyncWebhooksResource(self)
        self.with_raw_response = AsyncEInvoiceWithRawResponse(self)
        self.with_streaming_response = AsyncEInvoiceWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class EInvoiceWithRawResponse:
    def __init__(self, client: EInvoice) -> None:
        self.documents = documents.DocumentsResourceWithRawResponse(client.documents)
        self.inbox = inbox.InboxResourceWithRawResponse(client.inbox)
        self.outbox = outbox.OutboxResourceWithRawResponse(client.outbox)
        self.validate = validate.ValidateResourceWithRawResponse(client.validate)
        self.lookup = lookup.LookupResourceWithRawResponse(client.lookup)
        self.webhooks = webhooks.WebhooksResourceWithRawResponse(client.webhooks)


class AsyncEInvoiceWithRawResponse:
    def __init__(self, client: AsyncEInvoice) -> None:
        self.documents = documents.AsyncDocumentsResourceWithRawResponse(client.documents)
        self.inbox = inbox.AsyncInboxResourceWithRawResponse(client.inbox)
        self.outbox = outbox.AsyncOutboxResourceWithRawResponse(client.outbox)
        self.validate = validate.AsyncValidateResourceWithRawResponse(client.validate)
        self.lookup = lookup.AsyncLookupResourceWithRawResponse(client.lookup)
        self.webhooks = webhooks.AsyncWebhooksResourceWithRawResponse(client.webhooks)


class EInvoiceWithStreamedResponse:
    def __init__(self, client: EInvoice) -> None:
        self.documents = documents.DocumentsResourceWithStreamingResponse(client.documents)
        self.inbox = inbox.InboxResourceWithStreamingResponse(client.inbox)
        self.outbox = outbox.OutboxResourceWithStreamingResponse(client.outbox)
        self.validate = validate.ValidateResourceWithStreamingResponse(client.validate)
        self.lookup = lookup.LookupResourceWithStreamingResponse(client.lookup)
        self.webhooks = webhooks.WebhooksResourceWithStreamingResponse(client.webhooks)


class AsyncEInvoiceWithStreamedResponse:
    def __init__(self, client: AsyncEInvoice) -> None:
        self.documents = documents.AsyncDocumentsResourceWithStreamingResponse(client.documents)
        self.inbox = inbox.AsyncInboxResourceWithStreamingResponse(client.inbox)
        self.outbox = outbox.AsyncOutboxResourceWithStreamingResponse(client.outbox)
        self.validate = validate.AsyncValidateResourceWithStreamingResponse(client.validate)
        self.lookup = lookup.AsyncLookupResourceWithStreamingResponse(client.lookup)
        self.webhooks = webhooks.AsyncWebhooksResourceWithStreamingResponse(client.webhooks)


Client = EInvoice

AsyncClient = AsyncEInvoice
