from __future__ import annotations

import os
import contextlib
from typing import Any, Dict, ContextManager
from datetime import date, datetime, timezone

import httpx
import pytest
from respx import MockRouter

from tests.utils import serve_pages, page_payload, sent_queries
from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import DocumentResponse
from e_invoice_api.pagination import SyncDocumentsNumberPage, AsyncDocumentsNumberPage
from e_invoice_api.resources.outbox import (
    OutboxResourceWithRawResponse,
    AsyncOutboxResourceWithRawResponse,
    OutboxResourceWithStreamingResponse,
    AsyncOutboxResourceWithStreamingResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

SENT_DOCUMENT: Dict[str, Any] = {
    "id": "doc_out_01",
    "created_at": "2026-01-02T03:04:05Z",
    "direction": "OUTBOUND",
    "document_type": "INVOICE",
    "state": "SENT",
    "invoice_id": "OUT-2026-001",
    "invoice_date": "2026-01-02",
    "due_date": "2026-02-01",
    "currency": "EUR",
    "vendor_name": "Tenant NV",
    "customer_name": "Customer BV",
    "customer_peppol_id": "0208:0123456789",
    "invoice_total": "242.00",
    "subtotal": "200.00",
    "total_tax": "42.00",
    "items": [
        {"description": "Licence", "quantity": "1", "unit_price": "200.00", "amount": "200.00", "tax_rate": "21"},
    ],
    "tax_details": [{"amount": "42.00", "rate": "21"}],
}

DRAFT_DOCUMENT: Dict[str, Any] = {
    "id": "doc_out_02",
    "created_at": "2026-02-03T10:00:00Z",
    "direction": "OUTBOUND",
    "document_type": "CREDIT_NOTE",
    "state": "DRAFT",
    "customer_name": "Customer BV",
}

MINIMAL_DOCUMENT: Dict[str, Any] = {
    "id": "doc_out_03",
    "created_at": "2026-03-04T05:06:07Z",
}

# (method name, path) for every list endpoint on the outbox resource.
LIST_ENDPOINTS = [
    ("list_draft_documents", "/api/outbox/drafts"),
    ("list_received_documents", "/api/outbox/"),
]
parametrize_endpoints = pytest.mark.parametrize(
    ("method", "path"), LIST_ENDPOINTS, ids=[name for name, _ in LIST_ENDPOINTS]
)


def deprecation_of(method: str) -> ContextManager[object]:
    """`list_draft_documents` is marked `@deprecated`, so calling it must emit a DeprecationWarning."""
    if method == "list_draft_documents":
        return pytest.deprecated_call(match="^deprecated$")
    return contextlib.nullcontext()


def assert_sent_document(document: DocumentResponse) -> None:
    assert isinstance(document, DocumentResponse)
    assert document.id == "doc_out_01"
    assert document.created_at == datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    assert document.direction == "OUTBOUND"
    assert document.document_type == "INVOICE"
    assert document.state == "SENT"
    assert document.invoice_id == "OUT-2026-001"
    assert document.invoice_date == date(2026, 1, 2)
    assert document.due_date == date(2026, 2, 1)
    assert document.currency == "EUR"
    assert document.customer_name == "Customer BV"
    assert document.customer_peppol_id == "0208:0123456789"
    assert document.invoice_total == "242.00"
    assert document.items is not None
    assert [(i.description, i.quantity, i.unit_price, i.amount) for i in document.items] == [
        ("Licence", "1", "200.00", "200.00")
    ]
    assert document.tax_details is not None
    assert [(t.amount, t.rate) for t in document.tax_details] == [("42.00", "21")]


def assert_draft_document(document: DocumentResponse) -> None:
    assert isinstance(document, DocumentResponse)
    assert document.id == "doc_out_02"
    assert document.created_at == datetime(2026, 2, 3, 10, 0, 0, tzinfo=timezone.utc)
    assert document.document_type == "CREDIT_NOTE"
    assert document.state == "DRAFT"
    assert document.invoice_id is None
    assert document.items is None


def assert_minimal_document(document: DocumentResponse) -> None:
    assert isinstance(document, DocumentResponse)
    assert document.id == "doc_out_03"
    assert document.created_at == datetime(2026, 3, 4, 5, 6, 7, tzinfo=timezone.utc)
    assert document.direction is None
    assert document.state is None
    assert document.document_type is None


class TestOutbox:
    def test_resource_exposes_wrapper_properties(self, client: EInvoice) -> None:
        raw = client.outbox.with_raw_response
        streaming = client.outbox.with_streaming_response

        assert isinstance(raw, OutboxResourceWithRawResponse)
        assert isinstance(streaming, OutboxResourceWithStreamingResponse)
        # cached_property: the same wrapper is returned on every access.
        assert client.outbox.with_raw_response is raw
        assert client.outbox.with_streaming_response is streaming

    @pytest.mark.respx(base_url=base_url)
    def test_list_draft_documents_sends_all_filters(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/outbox/drafts").mock(
            return_value=httpx.Response(200, json=page_payload([], page=2))
        )

        with pytest.deprecated_call(match="^deprecated$"):
            client.outbox.list_draft_documents(  # ty: ignore[deprecated]
                page=2,
                page_size=20,
                search="OUT-2026",
                sort_by="invoice_date",
                sort_order="asc",
                state="FAILED",
                type="DEBIT_NOTE",
            )

        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/outbox/drafts"
        assert dict(request.url.params) == {
            "page": "2",
            "page_size": "20",
            "search": "OUT-2026",
            "sort_by": "invoice_date",
            "sort_order": "asc",
            "state": "FAILED",
            "type": "DEBIT_NOTE",
        }

    @pytest.mark.respx(base_url=base_url)
    def test_list_received_documents_sends_all_filters(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/outbox/").mock(return_value=httpx.Response(200, json=page_payload([], page=5)))

        client.outbox.list_received_documents(
            date_from=datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            date_to="2026-01-31T23:59:59Z",
            page=5,
            page_size=15,
            receiver="0208:0123456789",
            search="licence",
            sender="snd_123",
            sort_by="customer_name",
            sort_order="desc",
            type="INVOICE",
        )

        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/outbox/"
        assert dict(request.url.params) == {
            "date_from": "2026-01-01T00:00:00+00:00",
            "date_to": "2026-01-31T23:59:59Z",
            "page": "5",
            "page_size": "15",
            "receiver": "0208:0123456789",
            "search": "licence",
            "sender": "snd_123",
            "sort_by": "customer_name",
            "sort_order": "desc",
            "type": "INVOICE",
        }

    @pytest.mark.respx(base_url=base_url)
    def test_none_filters_are_omitted(self, respx_mock: MockRouter, client: EInvoice) -> None:
        drafts = respx_mock.get("/api/outbox/drafts").mock(return_value=httpx.Response(200, json=page_payload([])))
        sent = respx_mock.get("/api/outbox/").mock(return_value=httpx.Response(200, json=page_payload([])))

        with pytest.deprecated_call(match="^deprecated$"):
            client.outbox.list_draft_documents(search=None, state=None, type=None, page=1)  # ty: ignore[deprecated]
        client.outbox.list_received_documents(
            date_from=None, date_to=None, receiver=None, search=None, sender=None, type=None, page=1
        )

        assert dict(drafts.calls.last.request.url.params) == {"page": "1"}
        assert dict(sent.calls.last.request.url.params) == {"page": "1"}

    @pytest.mark.respx(base_url=base_url)
    @parametrize_endpoints
    def test_without_arguments_sends_no_query(
        self, respx_mock: MockRouter, client: EInvoice, method: str, path: str
    ) -> None:
        route = respx_mock.get(path).mock(return_value=httpx.Response(200, json=page_payload([])))

        with deprecation_of(method):
            getattr(client.outbox, method)()

        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == path
        assert request.url.query == b""

    @pytest.mark.respx(base_url=base_url)
    def test_list_draft_documents_parses_page(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/outbox/drafts").mock(
            return_value=httpx.Response(200, json=page_payload([DRAFT_DOCUMENT, MINIMAL_DOCUMENT]))
        )

        with pytest.deprecated_call(match="^deprecated$"):
            page = client.outbox.list_draft_documents()  # ty: ignore[deprecated]

        assert isinstance(page, SyncDocumentsNumberPage)
        assert page.page == 1
        assert page.page_size == 2
        assert page.total == 2
        assert page.has_next_page() is False
        assert len(page.items) == 2
        assert_draft_document(page.items[0])
        assert_minimal_document(page.items[1])

    @pytest.mark.respx(base_url=base_url)
    def test_list_received_documents_parses_page(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/outbox/").mock(
            return_value=httpx.Response(200, json=page_payload([SENT_DOCUMENT, MINIMAL_DOCUMENT], page=1, pages=3))
        )

        page = client.outbox.list_received_documents()

        assert isinstance(page, SyncDocumentsNumberPage)
        assert page.pages == 3
        assert page.has_next_page() is True
        assert len(page.items) == 2
        assert_sent_document(page.items[0])
        assert_minimal_document(page.items[1])

    @pytest.mark.respx(base_url=base_url)
    @parametrize_endpoints
    def test_auto_paginates_until_last_page(
        self, respx_mock: MockRouter, client: EInvoice, method: str, path: str
    ) -> None:
        route = respx_mock.get(path).mock(side_effect=serve_pages([SENT_DOCUMENT, DRAFT_DOCUMENT, MINIMAL_DOCUMENT]))

        with deprecation_of(method):
            documents = list(getattr(client.outbox, method)(page_size=1, type="INVOICE"))

        assert all(isinstance(document, DocumentResponse) for document in documents)
        assert [document.id for document in documents] == ["doc_out_01", "doc_out_02", "doc_out_03"]
        assert sent_queries(route) == [
            {"page_size": "1", "type": "INVOICE"},
            {"page_size": "1", "type": "INVOICE", "page": "2"},
            {"page_size": "1", "type": "INVOICE", "page": "3"},
        ]

    @pytest.mark.respx(base_url=base_url)
    @parametrize_endpoints
    def test_raw_response(self, respx_mock: MockRouter, client: EInvoice, method: str, path: str) -> None:
        respx_mock.get(path).mock(
            return_value=httpx.Response(200, json=page_payload([SENT_DOCUMENT]), headers={"x-request-id": "req_1"})
        )

        with deprecation_of(method):
            response = getattr(client.outbox.with_raw_response, method)()

        assert response.is_closed is True
        assert response.http_request.url.path == path
        assert response.headers["x-request-id"] == "req_1"
        page = response.parse()
        assert isinstance(page, SyncDocumentsNumberPage)
        assert len(page.items) == 1
        assert_sent_document(page.items[0])

    @pytest.mark.respx(base_url=base_url)
    @parametrize_endpoints
    def test_streaming_response(self, respx_mock: MockRouter, client: EInvoice, method: str, path: str) -> None:
        respx_mock.get(path).mock(return_value=httpx.Response(200, json=page_payload([DRAFT_DOCUMENT])))

        with deprecation_of(method), getattr(client.outbox.with_streaming_response, method)() as response:
            assert not response.is_closed
            assert response.http_request.url.path == path
            page = response.parse()
            assert isinstance(page, SyncDocumentsNumberPage)
            assert len(page.items) == 1
            assert_draft_document(page.items[0])

        assert response.is_closed is True


class TestAsyncOutbox:
    def test_resource_exposes_wrapper_properties(self, async_client: AsyncEInvoice) -> None:
        raw = async_client.outbox.with_raw_response
        streaming = async_client.outbox.with_streaming_response

        assert isinstance(raw, AsyncOutboxResourceWithRawResponse)
        assert isinstance(streaming, AsyncOutboxResourceWithStreamingResponse)
        assert async_client.outbox.with_raw_response is raw
        assert async_client.outbox.with_streaming_response is streaming

    @pytest.mark.respx(base_url=base_url)
    async def test_list_draft_documents_sends_all_filters(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.get("/api/outbox/drafts").mock(
            return_value=httpx.Response(200, json=page_payload([DRAFT_DOCUMENT]))
        )

        with pytest.deprecated_call(match="^deprecated$"):
            page = await async_client.outbox.list_draft_documents(  # ty: ignore[deprecated]
                page=1,
                page_size=5,
                search="draft",
                sort_by="created_at",
                sort_order="desc",
                state="DRAFT",
                type="CREDIT_NOTE",
            )

        assert isinstance(page, AsyncDocumentsNumberPage)
        assert_draft_document(page.items[0])
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/outbox/drafts"
        assert dict(request.url.params) == {
            "page": "1",
            "page_size": "5",
            "search": "draft",
            "sort_by": "created_at",
            "sort_order": "desc",
            "state": "DRAFT",
            "type": "CREDIT_NOTE",
        }

    @pytest.mark.respx(base_url=base_url)
    async def test_list_received_documents_sends_all_filters(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.get("/api/outbox/").mock(
            return_value=httpx.Response(200, json=page_payload([SENT_DOCUMENT]))
        )

        page = await async_client.outbox.list_received_documents(
            date_from="2026-03-01",
            date_to=datetime(2026, 3, 31, 12, 30, 0, tzinfo=timezone.utc),
            page=2,
            page_size=30,
            receiver="Customer BV",
            search="OUT",
            sender="snd_456",
            sort_by="invoice_id",
            sort_order="asc",
            type="SELFBILLING_CREDIT_NOTE",
        )

        assert isinstance(page, AsyncDocumentsNumberPage)
        assert_sent_document(page.items[0])
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/outbox/"
        assert dict(request.url.params) == {
            "date_from": "2026-03-01",
            "date_to": "2026-03-31T12:30:00+00:00",
            "page": "2",
            "page_size": "30",
            "receiver": "Customer BV",
            "search": "OUT",
            "sender": "snd_456",
            "sort_by": "invoice_id",
            "sort_order": "asc",
            "type": "SELFBILLING_CREDIT_NOTE",
        }

    @pytest.mark.respx(base_url=base_url)
    @parametrize_endpoints
    async def test_without_arguments_sends_no_query(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice, method: str, path: str
    ) -> None:
        route = respx_mock.get(path).mock(
            return_value=httpx.Response(200, json=page_payload([SENT_DOCUMENT, MINIMAL_DOCUMENT]))
        )

        with deprecation_of(method):
            page = await getattr(async_client.outbox, method)()

        assert isinstance(page, AsyncDocumentsNumberPage)
        assert_sent_document(page.items[0])
        assert_minimal_document(page.items[1])
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == path
        assert request.url.query == b""

    @pytest.mark.respx(base_url=base_url)
    @parametrize_endpoints
    async def test_auto_paginates_until_last_page(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice, method: str, path: str
    ) -> None:
        route = respx_mock.get(path).mock(side_effect=serve_pages([SENT_DOCUMENT, DRAFT_DOCUMENT, MINIMAL_DOCUMENT]))

        with deprecation_of(method):
            documents = [document async for document in getattr(async_client.outbox, method)(page_size=1)]

        assert all(isinstance(document, DocumentResponse) for document in documents)
        assert [document.id for document in documents] == ["doc_out_01", "doc_out_02", "doc_out_03"]
        assert sent_queries(route) == [
            {"page_size": "1"},
            {"page_size": "1", "page": "2"},
            {"page_size": "1", "page": "3"},
        ]

    @pytest.mark.respx(base_url=base_url)
    @parametrize_endpoints
    async def test_raw_response(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice, method: str, path: str
    ) -> None:
        respx_mock.get(path).mock(
            return_value=httpx.Response(200, json=page_payload([SENT_DOCUMENT]), headers={"x-request-id": "req_2"})
        )

        with deprecation_of(method):
            response = await getattr(async_client.outbox.with_raw_response, method)()

        assert response.is_closed is True
        assert response.http_request.url.path == path
        assert response.headers["x-request-id"] == "req_2"
        page = await response.parse()
        assert isinstance(page, AsyncDocumentsNumberPage)
        assert_sent_document(page.items[0])

    @pytest.mark.respx(base_url=base_url)
    @parametrize_endpoints
    async def test_streaming_response(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice, method: str, path: str
    ) -> None:
        respx_mock.get(path).mock(return_value=httpx.Response(200, json=page_payload([DRAFT_DOCUMENT])))

        with deprecation_of(method):
            stream = getattr(async_client.outbox.with_streaming_response, method)()
        async with stream as response:
            assert not response.is_closed
            assert response.http_request.url.path == path
            page = await response.parse()
            assert isinstance(page, AsyncDocumentsNumberPage)
            assert_draft_document(page.items[0])

        assert response.is_closed is True
