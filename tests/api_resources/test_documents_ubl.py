from __future__ import annotations

import os
import json
from typing import Any, Dict
from datetime import date, datetime, timezone

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, AsyncEInvoice, UnprocessableEntityError
from e_invoice_api.types import DocumentResponse
from e_invoice_api._response import APIResponse, AsyncAPIResponse
from e_invoice_api.types.documents import UblGetResponse
from e_invoice_api.resources.documents.ubl import (
    UblResourceWithRawResponse,
    AsyncUblResourceWithRawResponse,
    UblResourceWithStreamingResponse,
    AsyncUblResourceWithStreamingResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

UBL_BYTES = (
    b'<?xml version="1.0" encoding="UTF-8"?>\n'
    b'<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">'
    b"<cbc:ID>INV-2026-001</cbc:ID></Invoice>"
)

DOCUMENT_PAYLOAD: Dict[str, Any] = {
    "id": "doc_123",
    "created_at": "2026-02-03T10:11:12Z",
    "document_type": "INVOICE",
    "direction": "OUTBOUND",
    "state": "DRAFT",
    "invoice_id": "INV-2026-001",
    "invoice_date": "2026-02-03",
    "currency": "EUR",
    "invoice_total": "121.00",
    "vendor_name": "Acme BV",
    "customer_name": "Globex NV",
}

UBL_INFO: Dict[str, Any] = {
    "id": "ubl_01",
    "file_name": "INV-2026-001.xml",
    "file_hash": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
    "file_size": 4096,
    "receiver_peppol_id": "0123456789",
    "receiver_peppol_scheme": "0208",
    "sender_peppol_id": "1018265814",
    "sender_peppol_scheme": "0208",
    "signed_url": "https://storage.example.com/ubl_01.xml?signature=abc&expires=3600",
    "validated_at": "2026-02-03T10:15:00Z",
}

MINIMAL_UBL_INFO: Dict[str, Any] = {"id": "ubl_02", "file_name": "draft.xml"}


def assert_document(document: object) -> None:
    assert isinstance(document, DocumentResponse)
    assert document.id == "doc_123"
    assert document.created_at == datetime(2026, 2, 3, 10, 11, 12, tzinfo=timezone.utc)
    assert document.document_type == "INVOICE"
    assert document.direction == "OUTBOUND"
    assert document.state == "DRAFT"
    assert document.invoice_id == "INV-2026-001"
    assert document.invoice_date == date(2026, 2, 3)
    assert document.currency == "EUR"
    assert document.invoice_total == "121.00"
    assert document.vendor_name == "Acme BV"
    assert document.customer_name == "Globex NV"


def assert_ubl_info(info: object) -> None:
    assert isinstance(info, UblGetResponse)
    assert info.id == "ubl_01"
    assert info.file_name == "INV-2026-001.xml"
    assert info.file_hash == UBL_INFO["file_hash"]
    assert info.file_size == 4096
    assert info.receiver_peppol_id == "0123456789"
    assert info.receiver_peppol_scheme == "0208"
    assert info.sender_peppol_id == "1018265814"
    assert info.sender_peppol_scheme == "0208"
    assert info.signed_url == "https://storage.example.com/ubl_01.xml?signature=abc&expires=3600"
    assert info.validated_at == datetime(2026, 2, 3, 10, 15, 0, tzinfo=timezone.utc)


def assert_ubl_upload(request: httpx.Request) -> None:
    assert request.method == "POST"
    assert request.url.path == "/api/documents/ubl"
    assert request.url.query == b""
    assert request.headers["content-type"].startswith("multipart/form-data; boundary=")
    body = request.read()
    assert b'Content-Disposition: form-data; name="file"; filename="INV-2026-001.xml"' in body
    assert b"Content-Type: application/xml" in body
    assert UBL_BYTES in body


class TestUbl:
    def test_resource_exposes_wrapper_properties(self, client: EInvoice) -> None:
        raw = client.documents.ubl.with_raw_response
        streaming = client.documents.ubl.with_streaming_response

        assert isinstance(raw, UblResourceWithRawResponse)
        assert isinstance(streaming, UblResourceWithStreamingResponse)
        assert client.documents.ubl.with_raw_response is raw
        assert client.documents.ubl.with_streaming_response is streaming

    @pytest.mark.respx(base_url=base_url)
    def test_create_from_ubl_uploads_file_as_multipart(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/documents/ubl").mock(return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD))

        document = client.documents.ubl.create_from_ubl(file=("INV-2026-001.xml", UBL_BYTES, "application/xml"))

        assert route.call_count == 1
        assert_ubl_upload(route.calls.last.request)
        assert_document(document)

    @pytest.mark.respx(base_url=base_url)
    def test_create_from_ubl_accepts_raw_bytes(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/documents/ubl").mock(return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD))

        client.documents.ubl.create_from_ubl(file=UBL_BYTES)

        request = route.calls.last.request
        assert request.headers["content-type"].startswith("multipart/form-data; boundary=")
        body = request.read()
        assert b'Content-Disposition: form-data; name="file"; filename="upload"' in body
        assert UBL_BYTES in body

    @pytest.mark.respx(base_url=base_url)
    def test_create_from_ubl_validation_error(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.post("/api/documents/ubl").mock(
            return_value=httpx.Response(422, json={"detail": [{"msg": "Invalid UBL", "loc": ["body", "file"]}]})
        )

        with pytest.raises(UnprocessableEntityError) as exc_info:
            client.with_options(max_retries=0).documents.ubl.create_from_ubl(file=("bad.xml", b"<nope/>"))

        assert exc_info.value.status_code == 422

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create_from_ubl(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/documents/ubl").mock(
            return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD, headers={"x-request-id": "req_1"})
        )

        response = client.documents.ubl.with_raw_response.create_from_ubl(
            file=("INV-2026-001.xml", UBL_BYTES, "application/xml")
        )

        assert isinstance(response, APIResponse)
        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_1"
        assert_ubl_upload(route.calls.last.request)
        assert_document(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create_from_ubl(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/documents/ubl").mock(return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD))

        with client.documents.ubl.with_streaming_response.create_from_ubl(
            file=("INV-2026-001.xml", UBL_BYTES, "application/xml")
        ) as response:
            assert not response.is_closed
            assert_document(response.parse())

        assert response.is_closed is True
        assert_ubl_upload(route.calls.last.request)

    @pytest.mark.respx(base_url=base_url)
    def test_get_parses_ubl_metadata(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/documents/doc_123/ubl").mock(return_value=httpx.Response(200, json=UBL_INFO))

        info = client.documents.ubl.get("doc_123")

        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.query == b""
        assert request.content == b""
        assert request.headers["accept"] == "application/json"
        assert_ubl_info(info)

    @pytest.mark.respx(base_url=base_url)
    def test_get_parses_minimal_metadata(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/documents/doc_456/ubl").mock(return_value=httpx.Response(200, json=MINIMAL_UBL_INFO))

        info = client.documents.ubl.get("doc_456")

        assert info.id == "ubl_02"
        assert info.file_name == "draft.xml"
        assert info.file_hash is None
        assert info.file_size is None
        assert info.signed_url is None
        assert info.validated_at is None

    def test_get_rejects_empty_document_id(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.ubl.get("")

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_get_exposes_body_helpers(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/documents/doc_123/ubl").mock(return_value=httpx.Response(200, json=UBL_INFO))

        response = client.documents.ubl.with_raw_response.get("doc_123")

        assert isinstance(response, APIResponse)
        assert response.is_closed is True
        assert response.status_code == 200
        assert response.http_request.url.path == "/api/documents/doc_123/ubl"
        assert json.loads(response.read()) == UBL_INFO
        assert json.loads(response.text()) == UBL_INFO
        assert response.json() == UBL_INFO
        assert_ubl_info(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_get(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/documents/doc_123/ubl").mock(return_value=httpx.Response(200, json=UBL_INFO))

        with client.documents.ubl.with_streaming_response.get("doc_123") as response:
            assert not response.is_closed
            assert json.loads(b"".join(response.iter_bytes())) == UBL_INFO

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_get_parses(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/documents/doc_123/ubl").mock(return_value=httpx.Response(200, json=UBL_INFO))

        with client.documents.ubl.with_streaming_response.get("doc_123") as response:
            assert_ubl_info(response.parse())

        assert response.is_closed is True


class TestAsyncUbl:
    def test_resource_exposes_wrapper_properties(self, async_client: AsyncEInvoice) -> None:
        raw = async_client.documents.ubl.with_raw_response
        streaming = async_client.documents.ubl.with_streaming_response

        assert isinstance(raw, AsyncUblResourceWithRawResponse)
        assert isinstance(streaming, AsyncUblResourceWithStreamingResponse)
        assert async_client.documents.ubl.with_raw_response is raw
        assert async_client.documents.ubl.with_streaming_response is streaming

    @pytest.mark.respx(base_url=base_url)
    async def test_create_from_ubl_uploads_file_as_multipart(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.post("/api/documents/ubl").mock(return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD))

        document = await async_client.documents.ubl.create_from_ubl(
            file=("INV-2026-001.xml", UBL_BYTES, "application/xml")
        )

        assert route.call_count == 1
        assert_ubl_upload(route.calls.last.request)
        assert_document(document)

    @pytest.mark.respx(base_url=base_url)
    async def test_create_from_ubl_accepts_raw_bytes(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post("/api/documents/ubl").mock(return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD))

        await async_client.documents.ubl.create_from_ubl(file=UBL_BYTES)

        request = route.calls.last.request
        assert request.headers["content-type"].startswith("multipart/form-data; boundary=")
        body = request.read()
        assert b'Content-Disposition: form-data; name="file"; filename="upload"' in body
        assert UBL_BYTES in body

    @pytest.mark.respx(base_url=base_url)
    async def test_create_from_ubl_validation_error(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.post("/api/documents/ubl").mock(
            return_value=httpx.Response(422, json={"detail": [{"msg": "Invalid UBL", "loc": ["body", "file"]}]})
        )

        with pytest.raises(UnprocessableEntityError) as exc_info:
            await async_client.with_options(max_retries=0).documents.ubl.create_from_ubl(file=("bad.xml", b"<nope/>"))

        assert exc_info.value.status_code == 422

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create_from_ubl(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post("/api/documents/ubl").mock(
            return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD, headers={"x-request-id": "req_2"})
        )

        response = await async_client.documents.ubl.with_raw_response.create_from_ubl(
            file=("INV-2026-001.xml", UBL_BYTES, "application/xml")
        )

        assert isinstance(response, AsyncAPIResponse)
        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_2"
        assert_ubl_upload(route.calls.last.request)
        assert_document(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create_from_ubl(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.post("/api/documents/ubl").mock(return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD))

        async with async_client.documents.ubl.with_streaming_response.create_from_ubl(
            file=("INV-2026-001.xml", UBL_BYTES, "application/xml")
        ) as response:
            assert not response.is_closed
            assert_document(await response.parse())

        assert response.is_closed is True
        assert_ubl_upload(route.calls.last.request)

    @pytest.mark.respx(base_url=base_url)
    async def test_get_parses_ubl_metadata(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.get("/api/documents/doc_123/ubl").mock(return_value=httpx.Response(200, json=UBL_INFO))

        info = await async_client.documents.ubl.get("doc_123")

        assert route.call_count == 1
        assert route.calls.last.request.method == "GET"
        assert route.calls.last.request.url.query == b""
        assert_ubl_info(info)

    @pytest.mark.respx(base_url=base_url)
    async def test_get_parses_minimal_metadata(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/documents/doc_456/ubl").mock(return_value=httpx.Response(200, json=MINIMAL_UBL_INFO))

        info = await async_client.documents.ubl.get("doc_456")

        assert info.id == "ubl_02"
        assert info.file_name == "draft.xml"
        assert info.file_hash is None
        assert info.file_size is None
        assert info.signed_url is None
        assert info.validated_at is None

    async def test_get_rejects_empty_document_id(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.documents.ubl.get("")

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_get_exposes_body_helpers(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        respx_mock.get("/api/documents/doc_123/ubl").mock(return_value=httpx.Response(200, json=UBL_INFO))

        response = await async_client.documents.ubl.with_raw_response.get("doc_123")

        assert isinstance(response, AsyncAPIResponse)
        assert response.is_closed is True
        assert json.loads(await response.read()) == UBL_INFO
        assert json.loads(await response.text()) == UBL_INFO
        assert await response.json() == UBL_INFO
        assert_ubl_info(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_get(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/documents/doc_123/ubl").mock(return_value=httpx.Response(200, json=UBL_INFO))

        async with async_client.documents.ubl.with_streaming_response.get("doc_123") as response:
            assert not response.is_closed
            chunks = [chunk async for chunk in response.iter_bytes()]
            assert json.loads(b"".join(chunks)) == UBL_INFO

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_get_parses(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/documents/doc_123/ubl").mock(return_value=httpx.Response(200, json=UBL_INFO))

        async with async_client.documents.ubl.with_streaming_response.get("doc_123") as response:
            assert_ubl_info(await response.parse())

        assert response.is_closed is True
