from __future__ import annotations

import os
from typing import Any, Dict
from datetime import datetime, timezone

import httpx
import pytest
from respx import MockRouter

from tests.utils import serve_pages, page_payload, sent_queries
from e_invoice_api import EInvoice, AsyncEInvoice, ConflictError
from e_invoice_api.types import InboundEmail
from e_invoice_api._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)
from e_invoice_api.pagination import SyncDocumentsNumberPage, AsyncDocumentsNumberPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

FULL_EMAIL: Dict[str, Any] = {
    "id": "ie_01",
    "message_id": "<abc@mail.example.com>",
    "sender_email": "billing@supplier.example.com",
    "sender_name": "Supplier Billing",
    "to_addresses": "invoices@tenant.example.com",
    "cc_addresses": "cc@tenant.example.com",
    "bcc_addresses": None,
    "subject": "Invoice 2026-001",
    "attachments": [
        {"filename": "invoice.pdf", "size": 1024, "content_type": "application/pdf"},
        {"filename": "notes.txt"},
    ],
    "attachment_count": 2,
    "processed": True,
    "error_message": None,
    "received_at": "2026-01-02T03:04:05Z",
    "created_at": "2026-01-02T03:04:06Z",
    "processed_at": "2026-01-02T03:05:00Z",
    "document_id": "doc_123",
}

MINIMAL_EMAIL: Dict[str, Any] = {
    "id": "ie_02",
    "message_id": "<def@mail.example.com>",
    "sender_email": "other@supplier.example.com",
    "created_at": "2026-02-03T10:00:00Z",
}

PDF_BYTES = b"%PDF-1.7\n\x00\x01\xff binary body"


class TestMailbox:
    @pytest.mark.respx(base_url=base_url)
    def test_retrieve_parses_inbound_email(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/mailbox/ie_01").mock(return_value=httpx.Response(200, json=FULL_EMAIL))

        email = client.mailbox.retrieve("ie_01")

        assert route.call_count == 1
        assert isinstance(email, InboundEmail)
        assert email.id == "ie_01"
        assert email.message_id == "<abc@mail.example.com>"
        assert email.sender_email == "billing@supplier.example.com"
        assert email.sender_name == "Supplier Billing"
        assert email.to_addresses == "invoices@tenant.example.com"
        assert email.cc_addresses == "cc@tenant.example.com"
        assert email.bcc_addresses is None
        assert email.subject == "Invoice 2026-001"
        assert email.attachment_count == 2
        assert email.processed is True
        assert email.error_message is None
        assert email.received_at == datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
        assert email.created_at == datetime(2026, 1, 2, 3, 4, 6, tzinfo=timezone.utc)
        assert email.processed_at == datetime(2026, 1, 2, 3, 5, 0, tzinfo=timezone.utc)
        assert email.document_id == "doc_123"

        assert email.attachments is not None
        assert [a.filename for a in email.attachments] == ["invoice.pdf", "notes.txt"]
        assert email.attachments[0].size == 1024
        assert email.attachments[0].content_type == "application/pdf"
        assert email.attachments[1].size is None
        assert email.attachments[1].content_type is None

    def test_retrieve_rejects_empty_id(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `inbound_email_id` but received ''"):
            client.mailbox.retrieve("")

    @pytest.mark.respx(base_url=base_url)
    def test_list_sends_filters_as_query_string(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/mailbox/").mock(return_value=httpx.Response(200, json=page_payload([], page=2)))

        client.mailbox.list(
            page=2,
            page_size=50,
            status="failed",
            processed=False,
            received_from=datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            received_to="2026-01-31T23:59:59Z",
            search="invoice.pdf",
            sort_by="created_at",
            sort_order="asc",
        )

        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/mailbox/"
        assert dict(request.url.params) == {
            "page": "2",
            "page_size": "50",
            "status": "failed",
            "processed": "false",
            "received_from": "2026-01-01T00:00:00+00:00",
            "received_to": "2026-01-31T23:59:59Z",
            "search": "invoice.pdf",
            "sort_by": "created_at",
            "sort_order": "asc",
        }

    @pytest.mark.respx(base_url=base_url)
    def test_list_without_arguments_sends_no_query(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/mailbox/").mock(return_value=httpx.Response(200, json=page_payload([])))

        client.mailbox.list()

        assert route.calls.last.request.url.query == b""

    @pytest.mark.respx(base_url=base_url)
    def test_list_parses_page_of_inbound_emails(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/mailbox/").mock(
            return_value=httpx.Response(200, json=page_payload([FULL_EMAIL, MINIMAL_EMAIL]))
        )

        page = client.mailbox.list()

        assert isinstance(page, SyncDocumentsNumberPage)
        assert page.page == 1
        assert page.page_size == 2
        assert page.total == 2
        assert all(isinstance(item, InboundEmail) for item in page.items)
        assert [item.id for item in page.items] == ["ie_01", "ie_02"]
        minimal = page.items[1]
        assert minimal.created_at == datetime(2026, 2, 3, 10, 0, 0, tzinfo=timezone.utc)
        assert minimal.received_at is None
        assert minimal.sender_name is None
        assert minimal.document_id is None

    @pytest.mark.respx(base_url=base_url)
    def test_list_auto_paginates_until_last_page(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/mailbox/").mock(side_effect=serve_pages([FULL_EMAIL, MINIMAL_EMAIL]))

        ids = [email.id for email in client.mailbox.list(page_size=1, status="success")]

        assert ids == ["ie_01", "ie_02"]
        assert sent_queries(route) == [
            {"page_size": "1", "status": "success"},
            {"page_size": "1", "status": "success", "page": "2"},
        ]

    @pytest.mark.respx(base_url=base_url)
    def test_download_attachment_returns_binary_content(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/mailbox/ie_01/attachments/invoice.pdf").mock(
            return_value=httpx.Response(200, content=PDF_BYTES, headers={"content-type": "application/pdf"})
        )

        response = client.mailbox.download_attachment("invoice.pdf", inbound_email_id="ie_01")

        assert isinstance(response, BinaryAPIResponse)
        assert response.read() == PDF_BYTES
        assert response.headers["content-type"] == "application/pdf"
        assert response.status_code == 200
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.headers["accept"] == "*/*"

    @pytest.mark.respx(base_url=base_url)
    def test_download_attachment_escapes_filename_in_path(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get(url__regex=r".*/attachments/.*").mock(
            return_value=httpx.Response(200, content=b"hello", headers={"content-type": "text/plain"})
        )

        response = client.mailbox.download_attachment("my notes/v2.txt", inbound_email_id="ie_01")

        assert response.read() == b"hello"
        assert route.calls.last.request.url.raw_path == b"/api/mailbox/ie_01/attachments/my%20notes%2Fv2.txt"

    def test_download_attachment_rejects_empty_path_params(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `inbound_email_id` but received ''"):
            client.mailbox.download_attachment("invoice.pdf", inbound_email_id="")

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `filename` but received ''"):
            client.mailbox.download_attachment("", inbound_email_id="ie_01")

    @pytest.mark.respx(base_url=base_url)
    def test_reprocess_posts_and_parses_accepted_email(self, respx_mock: MockRouter, client: EInvoice) -> None:
        pending = {**FULL_EMAIL, "processed": False, "processed_at": None, "document_id": None}
        route = respx_mock.post("/api/mailbox/ie_01/reprocess").mock(return_value=httpx.Response(202, json=pending))

        email = client.mailbox.reprocess("ie_01")

        assert route.call_count == 1
        assert route.calls.last.request.content == b""
        assert isinstance(email, InboundEmail)
        assert email.id == "ie_01"
        assert email.processed is False
        assert email.processed_at is None
        assert email.document_id is None

    def test_reprocess_rejects_empty_id(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `inbound_email_id` but received ''"):
            client.mailbox.reprocess("")

    @pytest.mark.respx(base_url=base_url)
    def test_reprocess_conflict_raises_conflict_error(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.post("/api/mailbox/ie_01/reprocess").mock(
            return_value=httpx.Response(409, json={"message": "Email is not in a reprocessable state"})
        )

        with pytest.raises(ConflictError) as exc_info:
            client.with_options(max_retries=0).mailbox.reprocess("ie_01")

        assert exc_info.value.status_code == 409

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_exposes_headers_and_parsed_email(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/mailbox/ie_02").mock(
            return_value=httpx.Response(200, json=MINIMAL_EMAIL, headers={"x-request-id": "req_1"})
        )

        response = client.mailbox.with_raw_response.retrieve("ie_02")

        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_1"
        email = response.parse()
        assert isinstance(email, InboundEmail)
        assert email.sender_email == "other@supplier.example.com"

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list_parses_page(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/mailbox/").mock(return_value=httpx.Response(200, json=page_payload([MINIMAL_EMAIL])))

        response = client.mailbox.with_raw_response.list()

        page = response.parse()
        assert isinstance(page, SyncDocumentsNumberPage)
        assert [item.id for item in page.items] == ["ie_02"]

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_reprocess_reports_accepted(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.post("/api/mailbox/ie_02/reprocess").mock(return_value=httpx.Response(202, json=MINIMAL_EMAIL))

        response = client.mailbox.with_raw_response.reprocess("ie_02")

        assert response.status_code == 202
        assert response.parse().id == "ie_02"

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_download_attachment(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/mailbox/ie_01/attachments/invoice.pdf").mock(
            return_value=httpx.Response(200, content=PDF_BYTES, headers={"content-type": "application/pdf"})
        )

        response = client.mailbox.with_raw_response.download_attachment("invoice.pdf", inbound_email_id="ie_01")

        assert isinstance(response, BinaryAPIResponse)
        assert response.is_closed is True
        assert response.headers["content-type"] == "application/pdf"
        assert response.read() == PDF_BYTES

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_download_attachment(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/mailbox/ie_01/attachments/invoice.pdf").mock(
            return_value=httpx.Response(200, content=PDF_BYTES, headers={"content-type": "application/pdf"})
        )

        with client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            assert isinstance(response, StreamedBinaryAPIResponse)
            assert not response.is_closed
            assert response.headers["content-type"] == "application/pdf"
            assert b"".join(response.iter_bytes()) == PDF_BYTES

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/mailbox/ie_02").mock(return_value=httpx.Response(200, json=MINIMAL_EMAIL))

        with client.mailbox.with_streaming_response.retrieve("ie_02") as response:
            assert not response.is_closed
            email = response.parse()
            assert email.message_id == "<def@mail.example.com>"

        assert response.is_closed is True


class TestAsyncMailbox:
    @pytest.mark.respx(base_url=base_url)
    async def test_retrieve_parses_inbound_email(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.get("/api/mailbox/ie_01").mock(return_value=httpx.Response(200, json=FULL_EMAIL))

        email = await async_client.mailbox.retrieve("ie_01")

        assert route.call_count == 1
        assert isinstance(email, InboundEmail)
        assert email.subject == "Invoice 2026-001"
        assert email.received_at == datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
        assert email.attachments is not None
        assert email.attachments[0].filename == "invoice.pdf"

    async def test_path_params_reject_empty_values(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `inbound_email_id` but received ''"):
            await async_client.mailbox.retrieve("")

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `inbound_email_id` but received ''"):
            await async_client.mailbox.reprocess("")

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `inbound_email_id` but received ''"):
            await async_client.mailbox.download_attachment("invoice.pdf", inbound_email_id="")

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `filename` but received ''"):
            await async_client.mailbox.download_attachment("", inbound_email_id="ie_01")

    @pytest.mark.respx(base_url=base_url)
    async def test_list_sends_filters_as_query_string(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.get("/api/mailbox/").mock(
            return_value=httpx.Response(200, json=page_payload([MINIMAL_EMAIL]))
        )

        page = await async_client.mailbox.list(
            status="pending",
            processed=True,
            received_from=datetime(2026, 3, 4, 5, 6, 7, tzinfo=timezone.utc),
            sort_by="received_at",
            sort_order="desc",
        )

        assert isinstance(page, AsyncDocumentsNumberPage)
        assert [item.id for item in page.items] == ["ie_02"]
        assert dict(route.calls.last.request.url.params) == {
            "status": "pending",
            "processed": "true",
            "received_from": "2026-03-04T05:06:07+00:00",
            "sort_by": "received_at",
            "sort_order": "desc",
        }

    @pytest.mark.respx(base_url=base_url)
    async def test_list_auto_paginates_until_last_page(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.get("/api/mailbox/").mock(side_effect=serve_pages([FULL_EMAIL, MINIMAL_EMAIL]))

        ids = [email.id async for email in async_client.mailbox.list(page_size=1)]

        assert ids == ["ie_01", "ie_02"]
        assert sent_queries(route) == [
            {"page_size": "1"},
            {"page_size": "1", "page": "2"},
        ]

    @pytest.mark.respx(base_url=base_url)
    async def test_download_attachment_returns_binary_content(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.get("/api/mailbox/ie_01/attachments/invoice.pdf").mock(
            return_value=httpx.Response(200, content=PDF_BYTES, headers={"content-type": "application/pdf"})
        )

        response = await async_client.mailbox.download_attachment("invoice.pdf", inbound_email_id="ie_01")

        assert isinstance(response, AsyncBinaryAPIResponse)
        assert await response.read() == PDF_BYTES
        assert response.headers["content-type"] == "application/pdf"
        assert route.calls.last.request.headers["accept"] == "*/*"

    @pytest.mark.respx(base_url=base_url)
    async def test_reprocess_posts_and_parses_accepted_email(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.post("/api/mailbox/ie_02/reprocess").mock(
            return_value=httpx.Response(202, json=MINIMAL_EMAIL)
        )

        email = await async_client.mailbox.reprocess("ie_02")

        assert route.call_count == 1
        assert isinstance(email, InboundEmail)
        assert email.id == "ie_02"

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_exposes_headers_and_parsed_email(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        respx_mock.get("/api/mailbox/ie_02").mock(
            return_value=httpx.Response(200, json=MINIMAL_EMAIL, headers={"x-request-id": "req_2"})
        )

        response = await async_client.mailbox.with_raw_response.retrieve("ie_02")

        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_2"
        email = await response.parse()
        assert email.sender_email == "other@supplier.example.com"

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_reprocess_and_list(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.post("/api/mailbox/ie_02/reprocess").mock(return_value=httpx.Response(202, json=MINIMAL_EMAIL))
        respx_mock.get("/api/mailbox/").mock(return_value=httpx.Response(200, json=page_payload([FULL_EMAIL])))

        reprocessed = await async_client.mailbox.with_raw_response.reprocess("ie_02")
        listed = await async_client.mailbox.with_raw_response.list()

        assert reprocessed.status_code == 202
        assert (await reprocessed.parse()).id == "ie_02"
        page = await listed.parse()
        assert isinstance(page, AsyncDocumentsNumberPage)
        assert [item.id for item in page.items] == ["ie_01"]

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_download_attachment(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/mailbox/ie_01/attachments/invoice.pdf").mock(
            return_value=httpx.Response(200, content=PDF_BYTES, headers={"content-type": "application/pdf"})
        )

        response = await async_client.mailbox.with_raw_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        )

        assert isinstance(response, AsyncBinaryAPIResponse)
        assert response.headers["content-type"] == "application/pdf"
        assert await response.read() == PDF_BYTES

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_download_attachment(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        respx_mock.get("/api/mailbox/ie_01/attachments/invoice.pdf").mock(
            return_value=httpx.Response(200, content=PDF_BYTES, headers={"content-type": "application/pdf"})
        )

        async with async_client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            assert isinstance(response, AsyncStreamedBinaryAPIResponse)
            assert not response.is_closed
            chunks = [chunk async for chunk in response.iter_bytes()]
            assert b"".join(chunks) == PDF_BYTES

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/mailbox/ie_02").mock(return_value=httpx.Response(200, json=MINIMAL_EMAIL))

        async with async_client.mailbox.with_streaming_response.retrieve("ie_02") as response:
            assert not response.is_closed
            email = await response.parse()
            assert email.message_id == "<def@mail.example.com>"

        assert response.is_closed is True
