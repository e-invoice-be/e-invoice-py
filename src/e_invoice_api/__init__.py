import typing as _t

from . import types
from ._types import NOT_GIVEN, Omit, NoneType, NotGiven, Transport, ProxiesTypes, omit, not_given
from ._utils import file_from_path
from ._client import (
    Client,
    Stream,
    Timeout,
    EInvoice,
    AsyncClient,
    AsyncStream,
    AsyncEInvoice,
    RequestOptions,
)
from ._models import BaseModel
from ._version import __title__, __version__
from ._response import APIResponse as APIResponse, AsyncAPIResponse as AsyncAPIResponse
from ._constants import DEFAULT_TIMEOUT, DEFAULT_MAX_RETRIES, DEFAULT_CONNECTION_LIMITS
from ._exceptions import (
    APIError,
    ConflictError,
    EInvoiceError,
    NotFoundError,
    APIStatusError,
    RateLimitError,
    APITimeoutError,
    BadRequestError,
    APIConnectionError,
    AuthenticationError,
    InternalServerError,
    PermissionDeniedError,
    UnprocessableEntityError,
    APIResponseValidationError,
)
from ._base_client import DefaultHttpxClient, DefaultAioHttpClient, DefaultAsyncHttpxClient
from ._utils._logs import setup_logging as _setup_logging

__all__ = [
    "DEFAULT_CONNECTION_LIMITS",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_TIMEOUT",
    "NOT_GIVEN",
    "APIConnectionError",
    "APIError",
    "APIResponseValidationError",
    "APIStatusError",
    "APITimeoutError",
    "AsyncClient",
    "AsyncEInvoice",
    "AsyncStream",
    "AuthenticationError",
    "BadRequestError",
    "BaseModel",
    "Client",
    "ConflictError",
    "DefaultAioHttpClient",
    "DefaultAsyncHttpxClient",
    "DefaultHttpxClient",
    "EInvoice",
    "EInvoiceError",
    "InternalServerError",
    "NoneType",
    "NotFoundError",
    "NotGiven",
    "Omit",
    "PermissionDeniedError",
    "ProxiesTypes",
    "RateLimitError",
    "RequestOptions",
    "Stream",
    "Timeout",
    "Transport",
    "UnprocessableEntityError",
    "__title__",
    "__version__",
    "file_from_path",
    "not_given",
    "omit",
    "types",
]

if not _t.TYPE_CHECKING:
    from ._utils._resources_proxy import resources as resources

_setup_logging()

# Update the __module__ attribute for exported symbols so that
# error messages point to this module instead of the module
# it was originally defined in, e.g.
# e_invoice_api._exceptions.NotFoundError -> e_invoice_api.NotFoundError
__locals = locals()
for __name in __all__:
    if not __name.startswith("__"):
        try:
            __locals[__name].__module__ = "e_invoice_api"
        except (TypeError, AttributeError):
            # Some of our exported symbols are builtins which we can't set attributes for.
            pass
