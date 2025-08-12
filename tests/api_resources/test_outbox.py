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


class TestOutbox:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_draft_documents(self, client: EInvoice) -> None:
        outbox = client.outbox.list_draft_documents()
        assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], outbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_draft_documents_with_all_params(self, client: EInvoice) -> None:
        outbox = client.outbox.list_draft_documents(
            page=1,
            page_size=1,
        )
        assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], outbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list_draft_documents(self, client: EInvoice) -> None:
        response = client.outbox.with_raw_response.list_draft_documents()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        outbox = response.parse()
        assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], outbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list_draft_documents(self, client: EInvoice) -> None:
        with client.outbox.with_streaming_response.list_draft_documents() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            outbox = response.parse()
            assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], outbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_received_documents(self, client: EInvoice) -> None:
        outbox = client.outbox.list_received_documents()
        assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], outbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_received_documents_with_all_params(self, client: EInvoice) -> None:
        outbox = client.outbox.list_received_documents(
            date_from=parse_datetime("2019-12-27T18:11:19.117Z"),
            date_to=parse_datetime("2019-12-27T18:11:19.117Z"),
            page=1,
            page_size=1,
            search="search",
            sender="sender",
            state="DRAFT",
            type="INVOICE",
        )
        assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], outbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list_received_documents(self, client: EInvoice) -> None:
        response = client.outbox.with_raw_response.list_received_documents()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        outbox = response.parse()
        assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], outbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list_received_documents(self, client: EInvoice) -> None:
        with client.outbox.with_streaming_response.list_received_documents() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            outbox = response.parse()
            assert_matches_type(SyncDocumentsNumberPage[DocumentResponse], outbox, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncOutbox:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_draft_documents(self, async_client: AsyncEInvoice) -> None:
        outbox = await async_client.outbox.list_draft_documents()
        assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], outbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_draft_documents_with_all_params(self, async_client: AsyncEInvoice) -> None:
        outbox = await async_client.outbox.list_draft_documents(
            page=1,
            page_size=1,
        )
        assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], outbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list_draft_documents(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.outbox.with_raw_response.list_draft_documents()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        outbox = await response.parse()
        assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], outbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list_draft_documents(self, async_client: AsyncEInvoice) -> None:
        async with async_client.outbox.with_streaming_response.list_draft_documents() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            outbox = await response.parse()
            assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], outbox, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_received_documents(self, async_client: AsyncEInvoice) -> None:
        outbox = await async_client.outbox.list_received_documents()
        assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], outbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_received_documents_with_all_params(self, async_client: AsyncEInvoice) -> None:
        outbox = await async_client.outbox.list_received_documents(
            date_from=parse_datetime("2019-12-27T18:11:19.117Z"),
            date_to=parse_datetime("2019-12-27T18:11:19.117Z"),
            page=1,
            page_size=1,
            search="search",
            sender="sender",
            state="DRAFT",
            type="INVOICE",
        )
        assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], outbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list_received_documents(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.outbox.with_raw_response.list_received_documents()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        outbox = await response.parse()
        assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], outbox, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list_received_documents(self, async_client: AsyncEInvoice) -> None:
        async with async_client.outbox.with_streaming_response.list_received_documents() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            outbox = await response.parse()
            assert_matches_type(AsyncDocumentsNumberPage[DocumentResponse], outbox, path=["response"])

        assert cast(Any, response.is_closed) is True
