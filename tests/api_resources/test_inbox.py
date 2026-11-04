from __future__ import annotations

import os
from typing import Any, Dict
from datetime import date, datetime, timezone

import httpx
import pytest
from respx import MockRouter

from tests.utils import serve_pages, page_payload, sent_queries
from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import DocumentResponse
from e_invoice_api.pagination import SyncDocumentsNumberPage, AsyncDocumentsNumberPage
from e_invoice_api.resources.inbox import (
    InboxResourceWithRawResponse,
    AsyncInboxResourceWithRawResponse,
    InboxResourceWithStreamingResponse,
    AsyncInboxResourceWithStreamingResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

FULL_DOCUMENT: Dict[str, Any] = {
    "id": "doc_in_01",
    "created_at": "2026-01-02T03:04:05Z",
    "direction": "INBOUND",
    "document_type": "INVOICE",
    "state": "RECEIVED",
    "invoice_id": "INV-2026-001",
    "invoice_date": "2026-01-02",
    "due_date": "2026-02-01",
    "currency": "EUR",
    "vendor_name": "Supplier BV",
    "customer_name": "Tenant NV",
    "invoice_total": "121.00",
    "subtotal": "100.00",
    "total_tax": "21.00",
    "items": [
        {"description": "Consulting", "quantity": "2", "unit_price": "50.00", "amount": "100.00", "tax_rate": "21"},
    ],
    "tax_details": [{"amount": "21.00", "rate": "21"}],
    "payment_details": [{"iban": "BE68539007547034", "payment_reference": "+++090/9337/55493+++"}],
}

MINIMAL_DOCUMENT: Dict[str, Any] = {
    "id": "doc_in_02",
    "created_at": "2026-02-03T10:00:00Z",
}

CREDIT_NOTE: Dict[str, Any] = {
    "id": "doc_in_03",
    "created_at": "2026-03-04T05:06:07Z",
    "direction": "INBOUND",
    "document_type": "CREDIT_NOTE",
    "state": "RECEIVED",
    "preceding_invoice_id": "INV-2026-001",
    "preceding_invoice_date": "2026-01-02",
}

# (method name, path) for every list endpoint on the inbox resource.
LIST_ENDPOINTS = [
    ("list", "/api/inbox/"),
    ("list_credit_notes", "/api/inbox/credit-notes"),
    ("list_invoices", "/api/inbox/invoices"),
]
parametrize_endpoints = pytest.mark.parametrize(
    ("method", "path"), LIST_ENDPOINTS, ids=[name for name, _ in LIST_ENDPOINTS]
)
# Endpoints that only accept the shared paging and sorting parameters.
parametrize_sorted_endpoints = pytest.mark.parametrize(
    ("method", "path"), LIST_ENDPOINTS[1:], ids=[name for name, _ in LIST_ENDPOINTS[1:]]
)


def assert_full_document(document: DocumentResponse) -> None:
    assert isinstance(document, DocumentResponse)
    assert document.id == "doc_in_01"
    assert document.created_at == datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    assert document.direction == "INBOUND"
    assert document.document_type == "INVOICE"
    assert document.state == "RECEIVED"
    assert document.invoice_id == "INV-2026-001"
    assert document.invoice_date == date(2026, 1, 2)
    assert document.due_date == date(2026, 2, 1)
    assert document.currency == "EUR"
    assert document.vendor_name == "Supplier BV"
    assert document.customer_name == "Tenant NV"
    assert document.invoice_total == "121.00"
    assert document.subtotal == "100.00"
    assert document.total_tax == "21.00"
    assert document.items is not None
    assert [(i.description, i.quantity, i.unit_price, i.amount) for i in document.items] == [
        ("Consulting", "2", "50.00", "100.00")
    ]
    assert document.tax_details is not None
    assert [(t.amount, t.rate) for t in document.tax_details] == [("21.00", "21")]
    assert document.payment_details is not None
    assert document.payment_details[0].iban == "BE68539007547034"


def assert_minimal_document(document: DocumentResponse) -> None:
    assert isinstance(document, DocumentResponse)
    assert document.id == "doc_in_02"
    assert document.created_at == datetime(2026, 2, 3, 10, 0, 0, tzinfo=timezone.utc)
    assert document.direction is None
    assert document.document_type is None
    assert document.state is None
    assert document.invoice_date is None
    assert document.items is None


class TestInbox:
    def test_resource_exposes_wrapper_properties(self, client: EInvoice) -> None:
        raw = client.inbox.with_raw_response
        streaming = client.inbox.with_streaming_response

        assert isinstance(raw, InboxResourceWithRawResponse)
        assert isinstance(streaming, InboxResourceWithStreamingResponse)
        # cached_property: the same wrapper is returned on every access.
        assert client.inbox.with_raw_response is raw
        assert client.inbox.with_streaming_response is streaming

    @pytest.mark.respx(base_url=base_url)
    def test_list_sends_all_filters_as_query_string(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/inbox/").mock(return_value=httpx.Response(200, json=page_payload([], page=3)))

        client.inbox.list(
            date_from=datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            date_to="2026-01-31T23:59:59Z",
            page=3,
            page_size=25,
            search="INV-2026",
            sender="Supplier BV",
            sort_by="invoice_total",
            sort_order="asc",
            type="SELFBILLING_INVOICE",
        )

        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/inbox/"
        assert dict(request.url.params) == {
            "date_from": "2026-01-01T00:00:00+00:00",
            "date_to": "2026-01-31T23:59:59Z",
            "page": "3",
            "page_size": "25",
            "search": "INV-2026",
            "sender": "Supplier BV",
            "sort_by": "invoice_total",
            "sort_order": "asc",
            "type": "SELFBILLING_INVOICE",
        }

    @pytest.mark.respx(base_url=base_url)
    def test_list_omits_none_filters(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/inbox/").mock(return_value=httpx.Response(200, json=page_payload([])))

        client.inbox.list(date_from=None, date_to=None, search=None, sender=None, type=None, page_size=10)

        assert dict(route.calls.last.request.url.params) == {"page_size": "10"}

    @pytest.mark.respx(base_url=base_url)
    @parametrize_sorted_endpoints
    def test_sorted_list_sends_all_filters_as_query_string(
        self, respx_mock: MockRouter, client: EInvoice, method: str, path: str
    ) -> None:
        route = respx_mock.get(path).mock(return_value=httpx.Response(200, json=page_payload([], page=2)))

        getattr(client.inbox, method)(page=2, page_size=50, sort_by="due_date", sort_order="desc")

        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == path
        assert dict(request.url.params) == {
            "page": "2",
            "page_size": "50",
            "sort_by": "due_date",
            "sort_order": "desc",
        }

    @pytest.mark.respx(base_url=base_url)
    @parametrize_endpoints
    def test_without_arguments_sends_no_query(
        self, respx_mock: MockRouter, client: EInvoice, method: str, path: str
    ) -> None:
        route = respx_mock.get(path).mock(return_value=httpx.Response(200, json=page_payload([])))

        getattr(client.inbox, method)()

        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == path
        assert request.url.query == b""

    @pytest.mark.respx(base_url=base_url)
    def test_list_parses_page_of_documents(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/inbox/").mock(
            return_value=httpx.Response(200, json=page_payload([FULL_DOCUMENT, MINIMAL_DOCUMENT]))
        )

        page = client.inbox.list()

        assert isinstance(page, SyncDocumentsNumberPage)
        assert page.page == 1
        assert page.page_size == 2
        assert page.total == 2
        assert page.pages == 1
        assert page.has_next_page() is False
        assert len(page.items) == 2
        assert_full_document(page.items[0])
        assert_minimal_document(page.items[1])

    @pytest.mark.respx(base_url=base_url)
    def test_list_credit_notes_parses_page(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/inbox/credit-notes").mock(
            return_value=httpx.Response(200, json=page_payload([CREDIT_NOTE]))
        )

        page = client.inbox.list_credit_notes()

        assert isinstance(page, SyncDocumentsNumberPage)
        assert len(page.items) == 1
        credit_note = page.items[0]
        assert isinstance(credit_note, DocumentResponse)
        assert credit_note.document_type == "CREDIT_NOTE"
        assert credit_note.preceding_invoice_id == "INV-2026-001"
        assert credit_note.preceding_invoice_date == date(2026, 1, 2)

    @pytest.mark.respx(base_url=base_url)
    def test_list_invoices_parses_page(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/inbox/invoices").mock(return_value=httpx.Response(200, json=page_payload([FULL_DOCUMENT])))

        page = client.inbox.list_invoices()

        assert isinstance(page, SyncDocumentsNumberPage)
        assert len(page.items) == 1
        assert_full_document(page.items[0])

    @pytest.mark.respx(base_url=base_url)
    @parametrize_endpoints
    def test_auto_paginates_until_last_page(
        self, respx_mock: MockRouter, client: EInvoice, method: str, path: str
    ) -> None:
        route = respx_mock.get(path).mock(side_effect=serve_pages([FULL_DOCUMENT, MINIMAL_DOCUMENT, CREDIT_NOTE]))

        documents = list(getattr(client.inbox, method)(page_size=1, sort_order="asc"))

        assert all(isinstance(document, DocumentResponse) for document in documents)
        assert [document.id for document in documents] == ["doc_in_01", "doc_in_02", "doc_in_03"]
        assert sent_queries(route) == [
            {"page_size": "1", "sort_order": "asc"},
            {"page_size": "1", "sort_order": "asc", "page": "2"},
            {"page_size": "1", "sort_order": "asc", "page": "3"},
        ]

    @pytest.mark.respx(base_url=base_url)
    @parametrize_endpoints
    def test_raw_response(self, respx_mock: MockRouter, client: EInvoice, method: str, path: str) -> None:
        respx_mock.get(path).mock(
            return_value=httpx.Response(200, json=page_payload([FULL_DOCUMENT]), headers={"x-request-id": "req_1"})
        )

        response = getattr(client.inbox.with_raw_response, method)()

        assert response.is_closed is True
        assert response.http_request.url.path == path
        assert response.headers["x-request-id"] == "req_1"
        page = response.parse()
        assert isinstance(page, SyncDocumentsNumberPage)
        assert len(page.items) == 1
        assert_full_document(page.items[0])

    @pytest.mark.respx(base_url=base_url)
    @parametrize_endpoints
    def test_streaming_response(self, respx_mock: MockRouter, client: EInvoice, method: str, path: str) -> None:
        respx_mock.get(path).mock(return_value=httpx.Response(200, json=page_payload([MINIMAL_DOCUMENT])))

        with getattr(client.inbox.with_streaming_response, method)() as response:
            assert not response.is_closed
            assert response.http_request.url.path == path
            page = response.parse()
            assert isinstance(page, SyncDocumentsNumberPage)
            assert len(page.items) == 1
            assert_minimal_document(page.items[0])

        assert response.is_closed is True


class TestAsyncInbox:
    def test_resource_exposes_wrapper_properties(self, async_client: AsyncEInvoice) -> None:
        raw = async_client.inbox.with_raw_response
        streaming = async_client.inbox.with_streaming_response

        assert isinstance(raw, AsyncInboxResourceWithRawResponse)
        assert isinstance(streaming, AsyncInboxResourceWithStreamingResponse)
        assert async_client.inbox.with_raw_response is raw
        assert async_client.inbox.with_streaming_response is streaming

    @pytest.mark.respx(base_url=base_url)
    async def test_list_sends_all_filters_as_query_string(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.get("/api/inbox/").mock(
            return_value=httpx.Response(200, json=page_payload([MINIMAL_DOCUMENT]))
        )

        page = await async_client.inbox.list(
            date_from="2026-03-01",
            date_to=datetime(2026, 3, 31, 12, 30, 0, tzinfo=timezone.utc),
            page=1,
            page_size=100,
            search="credit",
            sender="BE0123456789",
            sort_by="vendor_name",
            sort_order="desc",
            type="CREDIT_NOTE",
        )

        assert isinstance(page, AsyncDocumentsNumberPage)
        assert_minimal_document(page.items[0])
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/inbox/"
        assert dict(request.url.params) == {
            "date_from": "2026-03-01",
            "date_to": "2026-03-31T12:30:00+00:00",
            "page": "1",
            "page_size": "100",
            "search": "credit",
            "sender": "BE0123456789",
            "sort_by": "vendor_name",
            "sort_order": "desc",
            "type": "CREDIT_NOTE",
        }

    @pytest.mark.respx(base_url=base_url)
    @parametrize_sorted_endpoints
    async def test_sorted_list_sends_all_filters_as_query_string(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice, method: str, path: str
    ) -> None:
        route = respx_mock.get(path).mock(return_value=httpx.Response(200, json=page_payload([CREDIT_NOTE])))

        page = await getattr(async_client.inbox, method)(
            page=4, page_size=10, sort_by="customer_name", sort_order="asc"
        )

        assert isinstance(page, AsyncDocumentsNumberPage)
        assert [item.id for item in page.items] == ["doc_in_03"]
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == path
        assert dict(request.url.params) == {
            "page": "4",
            "page_size": "10",
            "sort_by": "customer_name",
            "sort_order": "asc",
        }

    @pytest.mark.respx(base_url=base_url)
    @parametrize_endpoints
    async def test_without_arguments_sends_no_query(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice, method: str, path: str
    ) -> None:
        route = respx_mock.get(path).mock(
            return_value=httpx.Response(200, json=page_payload([FULL_DOCUMENT, MINIMAL_DOCUMENT]))
        )

        page = await getattr(async_client.inbox, method)()

        assert isinstance(page, AsyncDocumentsNumberPage)
        assert_full_document(page.items[0])
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
        route = respx_mock.get(path).mock(side_effect=serve_pages([FULL_DOCUMENT, MINIMAL_DOCUMENT, CREDIT_NOTE]))

        documents = [document async for document in getattr(async_client.inbox, method)(page_size=1)]

        assert all(isinstance(document, DocumentResponse) for document in documents)
        assert [document.id for document in documents] == ["doc_in_01", "doc_in_02", "doc_in_03"]
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
            return_value=httpx.Response(200, json=page_payload([FULL_DOCUMENT]), headers={"x-request-id": "req_2"})
        )

        response = await getattr(async_client.inbox.with_raw_response, method)()

        assert response.is_closed is True
        assert response.http_request.url.path == path
        assert response.headers["x-request-id"] == "req_2"
        page = await response.parse()
        assert isinstance(page, AsyncDocumentsNumberPage)
        assert_full_document(page.items[0])

    @pytest.mark.respx(base_url=base_url)
    @parametrize_endpoints
    async def test_streaming_response(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice, method: str, path: str
    ) -> None:
        respx_mock.get(path).mock(return_value=httpx.Response(200, json=page_payload([MINIMAL_DOCUMENT])))

        async with getattr(async_client.inbox.with_streaming_response, method)() as response:
            assert not response.is_closed
            assert response.http_request.url.path == path
            page = await response.parse()
            assert isinstance(page, AsyncDocumentsNumberPage)
            assert_minimal_document(page.items[0])

        assert response.is_closed is True
