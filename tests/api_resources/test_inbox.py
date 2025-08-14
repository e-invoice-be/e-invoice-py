# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import (
    DocumentResponse,
)
from e_invoice_api._utils import parse_datetime
from e_invoice_api.pagination import SyncDocumentsNumberPage, AsyncDocumentsNumberPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestInbox:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: EInvoice) -> None:
        inbox = client.inbox.list()
        assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: EInvoice) -> None:
        inbox = client.inbox.list(
            date_from=parse_datetime("2019-12-27T18:11:19.117Z"),
            date_to=parse_datetime("2019-12-27T18:11:19.117Z"),
            page=1,
            page_size=1,
            search="search",
            sender="sender",
            state="DRAFT",
            type="INVOICE",
        )
        assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: EInvoice) -> None:
        response = client.inbox.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inbox = response.parse()
        assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: EInvoice) -> None:
        with client.inbox.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            inbox = response.parse()
            assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_credit_notes(self, client: EInvoice) -> None:
        inbox = client.inbox.list_credit_notes()
        assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_credit_notes_with_all_params(self, client: EInvoice) -> None:
        inbox = client.inbox.list_credit_notes(
            page=1,
            page_size=1,
        )
        assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list_credit_notes(self, client: EInvoice) -> None:
        response = client.inbox.with_raw_response.list_credit_notes()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inbox = response.parse()
        assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list_credit_notes(self, client: EInvoice) -> None:
        with client.inbox.with_streaming_response.list_credit_notes() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            inbox = response.parse()
            assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_invoices(self, client: EInvoice) -> None:
        inbox = client.inbox.list_invoices()
        assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_invoices_with_all_params(self, client: EInvoice) -> None:
        inbox = client.inbox.list_invoices(
            page=1,
            page_size=1,
        )
        assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list_invoices(self, client: EInvoice) -> None:
        response = client.inbox.with_raw_response.list_invoices()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inbox = response.parse()
        assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list_invoices(self, client: EInvoice) -> None:
        with client.inbox.with_streaming_response.list_invoices() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            inbox = response.parse()
            assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncInbox:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncEInvoice) -> None:
        inbox = await async_client.inbox.list()
        assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEInvoice) -> None:
        inbox = await async_client.inbox.list(
            date_from=parse_datetime("2019-12-27T18:11:19.117Z"),
            date_to=parse_datetime("2019-12-27T18:11:19.117Z"),
            page=1,
            page_size=1,
            search="search",
            sender="sender",
            state="DRAFT",
            type="INVOICE",
        )
        assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.inbox.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inbox = await response.parse()
        assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEInvoice) -> None:
        async with async_client.inbox.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            inbox = await response.parse()
            assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_credit_notes(self, async_client: AsyncEInvoice) -> None:
        inbox = await async_client.inbox.list_credit_notes()
        assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_credit_notes_with_all_params(self, async_client: AsyncEInvoice) -> None:
        inbox = await async_client.inbox.list_credit_notes(
            page=1,
            page_size=1,
        )
        assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list_credit_notes(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.inbox.with_raw_response.list_credit_notes()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inbox = await response.parse()
        assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list_credit_notes(self, async_client: AsyncEInvoice) -> None:
        async with async_client.inbox.with_streaming_response.list_credit_notes() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            inbox = await response.parse()
            assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_invoices(self, async_client: AsyncEInvoice) -> None:
        inbox = await async_client.inbox.list_invoices()
        assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_invoices_with_all_params(self, async_client: AsyncEInvoice) -> None:
        inbox = await async_client.inbox.list_invoices(
            page=1,
            page_size=1,
        )
        assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list_invoices(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.inbox.with_raw_response.list_invoices()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inbox = await response.parse()
        assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list_invoices(self, async_client: AsyncEInvoice) -> None:
        async with async_client.inbox.with_streaming_response.list_invoices() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            inbox = await response.parse()
            assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], inbox, path=["response"])

        assert cast(Any, response.is_closed) is True
