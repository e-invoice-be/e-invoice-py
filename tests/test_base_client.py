"""Tests for the retry decisions and the `PageInfo` pagination paths in `_base_client`."""

from __future__ import annotations

import os
import json
from typing import Any, Dict, List, Generic, TypeVar, Optional, cast
from unittest import mock
from typing_extensions import override

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api._models import BaseModel
from e_invoice_api._exceptions import APIStatusError
from e_invoice_api._base_client import BasePage, PageInfo, BaseSyncPage, BaseAsyncPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

_T = TypeVar("_T")


def _no_retry_timeout(*_args: Any, **_kwargs: Any) -> float:
    return 0


# A response with one of these status codes is retried when the server sends no `x-should-retry` header.
RETRIED_STATUS_CODES = [408, 409, 429, 500, 502, 503, 504]
NOT_RETRIED_STATUS_CODES = [400, 401, 403, 404, 422]

# (status code, `x-should-retry` header, whether the client retries): the header overrides the status code.
SHOULD_RETRY_HEADER_CASES = [
    pytest.param(400, "true", True, id="true-overrides-400"),
    pytest.param(404, "true", True, id="true-overrides-404"),
    pytest.param(500, "false", False, id="false-overrides-500"),
    pytest.param(429, "false", False, id="false-overrides-429"),
    pytest.param(500, "maybe", True, id="other-value-falls-back-to-500"),
    pytest.param(400, "maybe", False, id="other-value-falls-back-to-400"),
]


def _fail_once(status_code: int, headers: Dict[str, str]) -> List[httpx.Response]:
    return [httpx.Response(status_code, headers=headers, json={}), httpx.Response(200, json={"ok": True})]


class Item(BaseModel):
    id: str


class SyncUrlPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    """Follows a `next_url` link: the url-based `PageInfo` branch."""

    items: List[_T]
    next_url: Optional[str] = None

    @override
    def _get_page_items(self) -> List[_T]:
        return self.items

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        if self.next_url is None:
            return None
        return PageInfo(url=httpx.URL(self.next_url))


class AsyncUrlPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    items: List[_T]
    next_url: Optional[str] = None

    @override
    def _get_page_items(self) -> List[_T]:
        return self.items

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        if self.next_url is None:
            return None
        return PageInfo(url=httpx.URL(self.next_url))


class SyncJsonPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    """Sends a `cursor` in the request body: the json-based `PageInfo` branch."""

    items: List[_T]
    next_cursor: Optional[str] = None

    @override
    def _get_page_items(self) -> List[_T]:
        return self.items

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        if self.next_cursor is None:
            return None
        return PageInfo(json={"cursor": self.next_cursor})


class AsyncJsonPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    items: List[_T]
    next_cursor: Optional[str] = None

    @override
    def _get_page_items(self) -> List[_T]:
        return self.items

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        if self.next_cursor is None:
            return None
        return PageInfo(json={"cursor": self.next_cursor})


def _serve_url_pages(request: httpx.Request) -> httpx.Response:
    if request.url.params.get("cursor") == "two":
        return httpx.Response(200, json={"items": [{"id": "b"}], "next_url": None})
    return httpx.Response(200, json={"items": [{"id": "a"}], "next_url": f"{base_url}/items?cursor=two"})


def _serve_json_pages(request: httpx.Request) -> httpx.Response:
    body = json.loads(request.content or b"{}")
    if isinstance(body, dict) and body.get("cursor") == "two":
        return httpx.Response(200, json={"items": [{"id": "b"}], "next_cursor": None})
    return httpx.Response(200, json={"items": [{"id": "a"}], "next_cursor": "two"})


def _sent_bodies(respx_mock: MockRouter) -> List[Any]:
    return [json.loads(call.request.content or b"null") for call in cast(Any, respx_mock.calls)]


def _sent_queries(respx_mock: MockRouter) -> List[Dict[str, str]]:
    return [dict(call.request.url.params) for call in cast(Any, respx_mock.calls)]


class TestRetryDecisions:
    @pytest.mark.parametrize("status_code", RETRIED_STATUS_CODES)
    @mock.patch("e_invoice_api._base_client.BaseClient._calculate_retry_timeout", _no_retry_timeout)
    @pytest.mark.respx(base_url=base_url)
    def test_retries_status_code(self, client: EInvoice, respx_mock: MockRouter, status_code: int) -> None:
        route = respx_mock.get("/retry").mock(side_effect=_fail_once(status_code, {}))

        response = client.with_options(max_retries=1).get("/retry", cast_to=httpx.Response)

        assert response.status_code == 200
        assert route.call_count == 2

    @pytest.mark.parametrize("status_code", NOT_RETRIED_STATUS_CODES)
    @mock.patch("e_invoice_api._base_client.BaseClient._calculate_retry_timeout", _no_retry_timeout)
    @pytest.mark.respx(base_url=base_url)
    def test_does_not_retry_status_code(self, client: EInvoice, respx_mock: MockRouter, status_code: int) -> None:
        route = respx_mock.get("/retry").mock(side_effect=_fail_once(status_code, {}))

        with pytest.raises(APIStatusError) as exc_info:
            client.with_options(max_retries=1).get("/retry", cast_to=httpx.Response)

        assert exc_info.value.status_code == status_code
        assert route.call_count == 1

    @pytest.mark.parametrize(("status_code", "header", "retried"), SHOULD_RETRY_HEADER_CASES)
    @mock.patch("e_invoice_api._base_client.BaseClient._calculate_retry_timeout", _no_retry_timeout)
    @pytest.mark.respx(base_url=base_url)
    def test_should_retry_header(
        self, client: EInvoice, respx_mock: MockRouter, status_code: int, header: str, retried: bool
    ) -> None:
        route = respx_mock.get("/retry").mock(side_effect=_fail_once(status_code, {"x-should-retry": header}))

        if retried:
            response = client.with_options(max_retries=1).get("/retry", cast_to=httpx.Response)
            assert response.status_code == 200
            assert route.call_count == 2
        else:
            with pytest.raises(APIStatusError) as exc_info:
                client.with_options(max_retries=1).get("/retry", cast_to=httpx.Response)
            assert exc_info.value.status_code == status_code
            assert route.call_count == 1


class TestAsyncRetryDecisions:
    @pytest.mark.parametrize("status_code", RETRIED_STATUS_CODES)
    @mock.patch("e_invoice_api._base_client.BaseClient._calculate_retry_timeout", _no_retry_timeout)
    @pytest.mark.respx(base_url=base_url)
    async def test_retries_status_code(
        self, async_client: AsyncEInvoice, respx_mock: MockRouter, status_code: int
    ) -> None:
        route = respx_mock.get("/retry").mock(side_effect=_fail_once(status_code, {}))

        response = await async_client.with_options(max_retries=1).get("/retry", cast_to=httpx.Response)

        assert response.status_code == 200
        assert route.call_count == 2

    @pytest.mark.parametrize("status_code", NOT_RETRIED_STATUS_CODES)
    @mock.patch("e_invoice_api._base_client.BaseClient._calculate_retry_timeout", _no_retry_timeout)
    @pytest.mark.respx(base_url=base_url)
    async def test_does_not_retry_status_code(
        self, async_client: AsyncEInvoice, respx_mock: MockRouter, status_code: int
    ) -> None:
        route = respx_mock.get("/retry").mock(side_effect=_fail_once(status_code, {}))

        with pytest.raises(APIStatusError) as exc_info:
            await async_client.with_options(max_retries=1).get("/retry", cast_to=httpx.Response)

        assert exc_info.value.status_code == status_code
        assert route.call_count == 1

    @pytest.mark.parametrize(("status_code", "header", "retried"), SHOULD_RETRY_HEADER_CASES)
    @mock.patch("e_invoice_api._base_client.BaseClient._calculate_retry_timeout", _no_retry_timeout)
    @pytest.mark.respx(base_url=base_url)
    async def test_should_retry_header(
        self, async_client: AsyncEInvoice, respx_mock: MockRouter, status_code: int, header: str, retried: bool
    ) -> None:
        route = respx_mock.get("/retry").mock(side_effect=_fail_once(status_code, {"x-should-retry": header}))

        if retried:
            response = await async_client.with_options(max_retries=1).get("/retry", cast_to=httpx.Response)
            assert response.status_code == 200
            assert route.call_count == 2
        else:
            with pytest.raises(APIStatusError) as exc_info:
                await async_client.with_options(max_retries=1).get("/retry", cast_to=httpx.Response)
            assert exc_info.value.status_code == status_code
            assert route.call_count == 1


class TestPageInfoPagination:
    @pytest.mark.respx(base_url=base_url)
    def test_url_based_next_page(self, client: EInvoice, respx_mock: MockRouter) -> None:
        respx_mock.get("/items").mock(side_effect=_serve_url_pages)

        page = client.get_api_list("/items", model=Item, page=SyncUrlPage[Item], options={"params": {"limit": 1}})
        ids = [item.id for item in page]

        assert ids == ["a", "b"]
        # the next-page url's query is merged with the original params
        assert _sent_queries(respx_mock) == [{"limit": "1"}, {"limit": "1", "cursor": "two"}]

    @pytest.mark.respx(base_url=base_url)
    def test_json_based_next_page_merges_into_body(self, client: EInvoice, respx_mock: MockRouter) -> None:
        respx_mock.post("/items").mock(side_effect=_serve_json_pages)

        page = client.get_api_list("/items", model=Item, page=SyncJsonPage[Item], body={"filter": "x"}, method="post")
        ids = [item.id for item in page]

        assert ids == ["a", "b"]
        assert _sent_bodies(respx_mock) == [{"filter": "x"}, {"filter": "x", "cursor": "two"}]

    @pytest.mark.respx(base_url=base_url)
    def test_json_based_next_page_without_body(self, client: EInvoice, respx_mock: MockRouter) -> None:
        respx_mock.post("/items").mock(side_effect=_serve_json_pages)

        page = client.get_api_list("/items", model=Item, page=SyncJsonPage[Item], method="post")
        ids = [item.id for item in page]

        assert ids == ["a", "b"]
        assert _sent_bodies(respx_mock) == [None, {"cursor": "two"}]

    @pytest.mark.respx(base_url=base_url)
    def test_json_based_next_page_rejects_non_mapping_info(self, client: EInvoice, respx_mock: MockRouter) -> None:
        respx_mock.post("/items").mock(side_effect=_serve_json_pages)
        page = client.get_api_list("/items", model=Item, page=SyncJsonPage[Item], method="post")

        with pytest.raises(TypeError, match="Pagination is only supported with mappings"):
            page._info_to_options(PageInfo(json=["two"]))

    @pytest.mark.respx(base_url=base_url)
    def test_json_based_next_page_rejects_non_mapping_body(self, client: EInvoice, respx_mock: MockRouter) -> None:
        respx_mock.post("/items").mock(side_effect=_serve_json_pages)
        page = client.get_api_list("/items", model=Item, page=SyncJsonPage[Item], body=["x"], method="post")

        with pytest.raises(TypeError, match="Pagination is only supported with mappings"):
            page._info_to_options(PageInfo(json={"cursor": "two"}))

    @pytest.mark.respx(base_url=base_url)
    def test_empty_page_info_is_rejected(self, client: EInvoice, respx_mock: MockRouter) -> None:
        respx_mock.get("/items").mock(side_effect=_serve_url_pages)
        page = client.get_api_list("/items", model=Item, page=SyncUrlPage[Item])

        with pytest.raises(ValueError, match="Unexpected PageInfo state"):
            page._info_to_options(cast(Any, PageInfo)())

    def test_page_info_repr(self) -> None:
        assert repr(PageInfo(url=httpx.URL("https://example.com/items?cursor=two"))) == (
            "PageInfo(url=https://example.com/items?cursor=two)"
        )
        assert repr(PageInfo(json={"cursor": "two"})) == "PageInfo(json={'cursor': 'two'})"
        assert repr(PageInfo(params={"page": 2})) == "PageInfo(params={'page': 2})"


class TestAsyncPageInfoPagination:
    @pytest.mark.respx(base_url=base_url)
    async def test_url_based_next_page(self, async_client: AsyncEInvoice, respx_mock: MockRouter) -> None:
        respx_mock.get("/items").mock(side_effect=_serve_url_pages)

        page = async_client.get_api_list(
            "/items", model=Item, page=AsyncUrlPage[Item], options={"params": {"limit": 1}}
        )
        ids = [item.id async for item in page]

        assert ids == ["a", "b"]
        assert _sent_queries(respx_mock) == [{"limit": "1"}, {"limit": "1", "cursor": "two"}]

    @pytest.mark.respx(base_url=base_url)
    async def test_json_based_next_page_merges_into_body(
        self, async_client: AsyncEInvoice, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/items").mock(side_effect=_serve_json_pages)

        page = async_client.get_api_list(
            "/items", model=Item, page=AsyncJsonPage[Item], body={"filter": "x"}, method="post"
        )
        ids = [item.id async for item in page]

        assert ids == ["a", "b"]
        assert _sent_bodies(respx_mock) == [{"filter": "x"}, {"filter": "x", "cursor": "two"}]
