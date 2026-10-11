from __future__ import annotations

import os
from typing import Any, Dict
from datetime import datetime, timezone

import httpx
import pytest
from respx import MockRouter

from tests.utils import serve_pages, page_payload, sent_queries
from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import DocumentResponse
from e_invoice_api.pagination import SyncDocumentsNumberPage, AsyncDocumentsNumberPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

DRAFT_INVOICE: Dict[str, Any] = {
    "id": "doc_draft_1",
    "created_at": "2026-04-01T08:30:00Z",
    "state": "DRAFT",
    "document_type": "INVOICE",
    "direction": "OUTBOUND",
    "invoice_id": "INV-2026-001",
    "invoice_total": "121.00",
    "currency": "EUR",
    "vendor_name": "Acme BV",
}

FAILED_CREDIT_NOTE: Dict[str, Any] = {
    "id": "doc_draft_2",
    "created_at": "2026-04-02T09:00:00Z",
    "state": "FAILED",
    "document_type": "CREDIT_NOTE",
}


class TestDrafts:
    @pytest.mark.respx(base_url=base_url)
    def test_list_parses_page_of_documents(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/drafts/").mock(
            return_value=httpx.Response(200, json=page_payload([DRAFT_INVOICE, FAILED_CREDIT_NOTE]))
        )

        page = client.drafts.list()

        assert route.call_count == 1
        assert route.calls.last.request.url.query == b""
        assert isinstance(page, SyncDocumentsNumberPage)
        assert page.page == 1
        assert page.total == 2
        assert all(isinstance(item, DocumentResponse) for item in page.items)
        first, second = page.items
        assert first.id == "doc_draft_1"
        assert first.created_at == datetime(2026, 4, 1, 8, 30, 0, tzinfo=timezone.utc)
        assert first.state == "DRAFT"
        assert first.document_type == "INVOICE"
        assert first.direction == "OUTBOUND"
        assert first.invoice_id == "INV-2026-001"
        assert first.invoice_total == "121.00"
        assert first.currency == "EUR"
        assert first.vendor_name == "Acme BV"
        assert second.id == "doc_draft_2"
        assert second.state == "FAILED"
        assert second.document_type == "CREDIT_NOTE"
        assert second.invoice_id is None

    @pytest.mark.respx(base_url=base_url)
    def test_list_sends_filters_as_query_string(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/drafts/").mock(return_value=httpx.Response(200, json=page_payload([], page=3)))

        client.drafts.list(
            page=3,
            page_size=25,
            state="FAILED",
            type="CREDIT_NOTE",
            date_from=datetime(2026, 4, 1, 0, 0, 0, tzinfo=timezone.utc),
            date_to="2026-04-30T23:59:59Z",
            search="Acme",
            sort_by="invoice_total",
            sort_order="asc",
        )

        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/drafts/"
        assert dict(request.url.params) == {
            "page": "3",
            "page_size": "25",
            "state": "FAILED",
            "type": "CREDIT_NOTE",
            "date_from": "2026-04-01T00:00:00+00:00",
            "date_to": "2026-04-30T23:59:59Z",
            "search": "Acme",
            "sort_by": "invoice_total",
            "sort_order": "asc",
        }

    @pytest.mark.respx(base_url=base_url)
    def test_list_auto_paginates_until_last_page(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/drafts/").mock(side_effect=serve_pages([DRAFT_INVOICE, FAILED_CREDIT_NOTE]))

        ids = [document.id for document in client.drafts.list(page_size=1, state="DRAFT")]

        assert ids == ["doc_draft_1", "doc_draft_2"]
        assert sent_queries(route) == [
            {"page_size": "1", "state": "DRAFT"},
            {"page_size": "1", "state": "DRAFT", "page": "2"},
        ]

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/drafts/").mock(
            return_value=httpx.Response(200, json=page_payload([DRAFT_INVOICE]), headers={"x-request-id": "req_d1"})
        )

        response = client.drafts.with_raw_response.list()

        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_d1"
        page = response.parse()
        assert isinstance(page, SyncDocumentsNumberPage)
        assert [item.invoice_id for item in page.items] == ["INV-2026-001"]

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/drafts/").mock(return_value=httpx.Response(200, json=page_payload([FAILED_CREDIT_NOTE])))

        with client.drafts.with_streaming_response.list() as response:
            assert not response.is_closed
            page = response.parse()
            assert [item.id for item in page.items] == ["doc_draft_2"]

        assert response.is_closed is True


class TestAsyncDrafts:
    @pytest.mark.respx(base_url=base_url)
    async def test_list_parses_page_and_sends_filters(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.get("/api/drafts/").mock(
            return_value=httpx.Response(200, json=page_payload([DRAFT_INVOICE, FAILED_CREDIT_NOTE]))
        )

        page = await async_client.drafts.list(
            type="INVOICE",
            date_from=datetime(2026, 4, 1, 12, 0, 0, tzinfo=timezone.utc),
            date_to=datetime(2026, 4, 30, 12, 0, 0, tzinfo=timezone.utc),
            sort_by="created_at",
        )

        assert isinstance(page, AsyncDocumentsNumberPage)
        assert all(isinstance(item, DocumentResponse) for item in page.items)
        assert [item.id for item in page.items] == ["doc_draft_1", "doc_draft_2"]
        assert page.items[0].state == "DRAFT"
        assert page.items[0].created_at == datetime(2026, 4, 1, 8, 30, 0, tzinfo=timezone.utc)
        request = route.calls.last.request
        assert request.url.path == "/api/drafts/"
        assert dict(request.url.params) == {
            "type": "INVOICE",
            "date_from": "2026-04-01T12:00:00+00:00",
            "date_to": "2026-04-30T12:00:00+00:00",
            "sort_by": "created_at",
        }

    @pytest.mark.respx(base_url=base_url)
    async def test_list_auto_paginates_until_last_page(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.get("/api/drafts/").mock(side_effect=serve_pages([DRAFT_INVOICE, FAILED_CREDIT_NOTE]))

        ids = [document.id async for document in async_client.drafts.list(page_size=1)]

        assert ids == ["doc_draft_1", "doc_draft_2"]
        assert sent_queries(route) == [
            {"page_size": "1"},
            {"page_size": "1", "page": "2"},
        ]

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/drafts/").mock(
            return_value=httpx.Response(200, json=page_payload([DRAFT_INVOICE]), headers={"x-request-id": "req_d2"})
        )

        response = await async_client.drafts.with_raw_response.list()

        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_d2"
        page = await response.parse()
        assert isinstance(page, AsyncDocumentsNumberPage)
        assert [item.invoice_id for item in page.items] == ["INV-2026-001"]

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/drafts/").mock(return_value=httpx.Response(200, json=page_payload([FAILED_CREDIT_NOTE])))

        async with async_client.drafts.with_streaming_response.list() as response:
            assert not response.is_closed
            page = await response.parse()
            assert [item.id for item in page.items] == ["doc_draft_2"]

        assert response.is_closed is True
