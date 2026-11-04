from __future__ import annotations

import os
import json
from typing import Any, Dict
from datetime import date, datetime, timezone

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import (
    DocumentResponse,
    UblDocumentValidation,
    DocumentDeleteResponse,
    DocumentCreateFromPdfResponse,
)
from e_invoice_api.resources.documents import (
    UblResource,
    AsyncUblResource,
    AttachmentsResource,
    AsyncAttachmentsResource,
    UblResourceWithRawResponse,
    AsyncUblResourceWithRawResponse,
    DocumentsResourceWithRawResponse,
    UblResourceWithStreamingResponse,
    AttachmentsResourceWithRawResponse,
    AsyncDocumentsResourceWithRawResponse,
    AsyncUblResourceWithStreamingResponse,
    DocumentsResourceWithStreamingResponse,
    AsyncAttachmentsResourceWithRawResponse,
    AttachmentsResourceWithStreamingResponse,
    AsyncDocumentsResourceWithStreamingResponse,
    AsyncAttachmentsResourceWithStreamingResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

PDF_BYTES = b"%PDF-1.7\n\x00\x01\xff fake invoice body"

DOCUMENT_PAYLOAD: Dict[str, Any] = {
    "id": "doc_123",
    "created_at": "2026-10-01T08:30:00Z",
    "document_type": "INVOICE",
    "state": "DRAFT",
    "direction": "OUTBOUND",
    "currency": "EUR",
    "invoice_id": "INV-2026-001",
    "invoice_date": "2026-10-01",
    "due_date": "2026-10-31",
    "customer_name": "Buyer NV",
    "vendor_name": "Acme BV",
    "subtotal": "100.00",
    "total_tax": "21.00",
    "invoice_total": "121.00",
    "items": [{"description": "Consulting", "quantity": "2", "unit_price": "50.00", "amount": "100.00"}],
    "tax_details": [{"rate": "21.00", "amount": "21.00"}],
}

SENT_DOCUMENT_PAYLOAD: Dict[str, Any] = {**DOCUMENT_PAYLOAD, "state": "SENT"}

PDF_RESULT_PAYLOAD: Dict[str, Any] = {
    "document_type": "CREDIT_NOTE",
    "direction": "INBOUND",
    "invoice_id": "CN-2026-007",
    "invoice_date": "2026-02-03",
    "vendor_tax_id": "BE1018265814",
    "customer_tax_id": "NL123456789B01",
    "invoice_total": "121.00",
    "items": [{"description": "Consulting", "amount": "100.00"}],
    "success": True,
    "error_message": None,
    "ubl_document": "<Invoice/>",
}

VALIDATION_PAYLOAD: Dict[str, Any] = {
    "id": "doc_123",
    "file_name": "doc_123.xml",
    "is_valid": False,
    "issues": [
        {
            "message": "Buyer reference or purchase order reference MUST be provided.",
            "schematron": "PEPPOL-EN16931",
            "type": "error",
            "flag": "fatal",
            "location": "/Invoice",
            "rule_id": "PEPPOL-EN16931-R003",
            "test": "cbc:BuyerReference or cac:OrderReference/cbc:ID",
        },
        {"message": "Minor issue", "schematron": "CEN-EN16931-UBL", "type": "warning"},
    ],
    "ubl_document": None,
}

CREATE_PARAMS: Dict[str, Any] = {
    "invoice_id": "INV-2026-001",
    "invoice_date": date(2026, 10, 1),
    "document_type": "INVOICE",
    "currency": "EUR",
    "customer_name": "Buyer NV",
    "items": [{"description": "Consulting", "quantity": 2, "unit_price": "50.00"}],
}

EXPECTED_CREATE_BODY: Dict[str, Any] = {
    "invoice_id": "INV-2026-001",
    "invoice_date": "2026-10-01",
    "document_type": "INVOICE",
    "currency": "EUR",
    "customer_name": "Buyer NV",
    "items": [{"description": "Consulting", "quantity": 2, "unit_price": "50.00"}],
}

SEND_PARAMS: Dict[str, Any] = {
    "receiver_peppol_id": "0208:0123456789",
    "receiver_peppol_scheme": "iso6523-actorid-upis",
    "sender_peppol_id": "0208:1018265814",
    "sender_peppol_scheme": "iso6523-actorid-upis",
}


def assert_document(document: DocumentResponse, *, state: str = "DRAFT") -> None:
    assert isinstance(document, DocumentResponse)
    assert document.id == "doc_123"
    assert document.created_at == datetime(2026, 10, 1, 8, 30, tzinfo=timezone.utc)
    assert document.document_type == "INVOICE"
    assert document.state == state
    assert document.direction == "OUTBOUND"
    assert document.currency == "EUR"
    assert document.invoice_id == "INV-2026-001"
    assert document.invoice_date == date(2026, 10, 1)
    assert document.due_date == date(2026, 10, 31)
    assert document.invoice_total == "121.00"
    assert document.items is not None
    assert [(item.description, item.quantity, item.amount) for item in document.items] == [
        ("Consulting", "2", "100.00")
    ]
    assert document.tax_details is not None
    assert document.tax_details[0].rate == "21.00"


def assert_pdf_result(result: DocumentCreateFromPdfResponse) -> None:
    assert isinstance(result, DocumentCreateFromPdfResponse)
    assert result.document_type == "CREDIT_NOTE"
    assert result.direction == "INBOUND"
    assert result.invoice_id == "CN-2026-007"
    assert result.invoice_date == date(2026, 2, 3)
    assert result.vendor_tax_id == "BE1018265814"
    assert result.customer_tax_id == "NL123456789B01"
    assert result.success is True
    assert result.error_message is None
    assert result.ubl_document == "<Invoice/>"
    assert result.items is not None
    assert result.items[0].amount == "100.00"


def assert_validation(validation: UblDocumentValidation) -> None:
    assert isinstance(validation, UblDocumentValidation)
    assert validation.id == "doc_123"
    assert validation.file_name == "doc_123.xml"
    assert validation.is_valid is False
    assert validation.ubl_document is None
    error, warning = validation.issues
    assert error.type == "error"
    assert error.rule_id == "PEPPOL-EN16931-R003"
    assert error.flag == "fatal"
    assert error.location == "/Invoice"
    assert error.test == "cbc:BuyerReference or cac:OrderReference/cbc:ID"
    assert warning.type == "warning"
    assert warning.schematron == "CEN-EN16931-UBL"
    assert warning.rule_id is None
    assert warning.flag is None


def assert_pdf_upload(request: httpx.Request) -> None:
    assert request.method == "POST"
    assert request.url.path == "/api/documents/pdf"
    assert request.headers["content-type"].startswith("multipart/form-data; boundary=")
    body = request.read()
    assert b'Content-Disposition: form-data; name="file"; filename="invoice.pdf"' in body
    assert b"Content-Type: application/pdf" in body
    assert PDF_BYTES in body


class TestDocuments:
    # create

    @pytest.mark.respx(base_url=base_url)
    def test_create_sends_json_body_and_construct_pdf_query(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/documents/").mock(return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD))

        document = client.documents.create(construct_pdf=True, **CREATE_PARAMS)

        request = route.calls.last.request
        assert request.method == "POST"
        assert request.url.path == "/api/documents/"
        assert dict(request.url.params) == {"construct_pdf": "true"}
        assert json.loads(request.content) == EXPECTED_CREATE_BODY
        assert_document(document)

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/documents/").mock(
            return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD, headers={"x-request-id": "req_1"})
        )

        response = client.documents.with_raw_response.create(**CREATE_PARAMS)

        assert response.is_closed is True
        assert response.status_code == 200
        assert response.headers["x-request-id"] == "req_1"
        assert route.calls.last.request.url.query == b""
        assert json.loads(route.calls.last.request.content) == EXPECTED_CREATE_BODY
        assert_document(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.post("/api/documents/").mock(return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD))

        with client.documents.with_streaming_response.create(**CREATE_PARAMS) as response:
            assert not response.is_closed
            assert_document(response.parse())

        assert response.is_closed is True

    # retrieve

    @pytest.mark.respx(base_url=base_url)
    def test_retrieve(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/documents/doc_123").mock(return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD))

        document = client.documents.retrieve("doc_123")

        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.query == b""
        assert request.content == b""
        assert_document(document)

    def test_retrieve_rejects_empty_document_id(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.retrieve("")

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/documents/doc_123").mock(
            return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD, headers={"x-request-id": "req_1"})
        )

        response = client.documents.with_raw_response.retrieve("doc_123")

        assert response.is_closed is True
        assert response.status_code == 200
        assert response.headers["x-request-id"] == "req_1"
        assert response.http_request.url.path == "/api/documents/doc_123"
        assert_document(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/documents/doc_123").mock(return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD))

        with client.documents.with_streaming_response.retrieve("doc_123") as response:
            assert not response.is_closed
            assert_document(response.parse())

        assert response.is_closed is True

    # delete

    @pytest.mark.respx(base_url=base_url)
    def test_delete(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.delete("/api/documents/doc_123").mock(
            return_value=httpx.Response(200, json={"is_deleted": True})
        )

        result = client.documents.delete("doc_123")

        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "DELETE"
        assert request.url.query == b""
        assert isinstance(result, DocumentDeleteResponse)
        assert result.is_deleted is True

    def test_delete_rejects_empty_document_id(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.delete("")

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.delete("/api/documents/doc_123").mock(
            return_value=httpx.Response(200, json={"is_deleted": False}, headers={"x-request-id": "req_1"})
        )

        response = client.documents.with_raw_response.delete("doc_123")

        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_1"
        assert response.http_request.method == "DELETE"
        result = response.parse()
        assert isinstance(result, DocumentDeleteResponse)
        assert result.is_deleted is False

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.delete("/api/documents/doc_123").mock(return_value=httpx.Response(200, json={"is_deleted": True}))

        with client.documents.with_streaming_response.delete("doc_123") as response:
            assert not response.is_closed
            result = response.parse()
            assert isinstance(result, DocumentDeleteResponse)
            assert result.is_deleted is True

        assert response.is_closed is True

    # create_from_pdf

    @pytest.mark.respx(base_url=base_url)
    def test_create_from_pdf_uploads_multipart_with_tax_id_query(
        self, respx_mock: MockRouter, client: EInvoice
    ) -> None:
        route = respx_mock.post("/api/documents/pdf").mock(return_value=httpx.Response(200, json=PDF_RESULT_PAYLOAD))

        result = client.documents.create_from_pdf(
            file=("invoice.pdf", PDF_BYTES, "application/pdf"),
            customer_tax_id="NL123456789B01",
            vendor_tax_id="BE1018265814",
        )

        request = route.calls.last.request
        assert_pdf_upload(request)
        assert dict(request.url.params) == {"customer_tax_id": "NL123456789B01", "vendor_tax_id": "BE1018265814"}
        # tax ids travel in the query string only, not as form fields
        assert b'name="customer_tax_id"' not in request.content
        assert b'name="vendor_tax_id"' not in request.content
        assert_pdf_result(result)

    @pytest.mark.respx(base_url=base_url)
    def test_create_from_pdf_without_tax_ids_sends_no_query(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/documents/pdf").mock(
            return_value=httpx.Response(200, json={"success": False, "error_type": "extraction", "items": []})
        )

        result = client.documents.create_from_pdf(file=("invoice.pdf", PDF_BYTES, "application/pdf"))

        request = route.calls.last.request
        assert_pdf_upload(request)
        assert request.url.query == b""
        assert result.success is False
        assert result.error_type == "extraction"
        assert result.items == []
        assert result.ubl_document is None

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create_from_pdf(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/documents/pdf").mock(
            return_value=httpx.Response(200, json=PDF_RESULT_PAYLOAD, headers={"x-request-id": "req_1"})
        )

        response = client.documents.with_raw_response.create_from_pdf(
            file=("invoice.pdf", PDF_BYTES, "application/pdf"), vendor_tax_id="BE1018265814"
        )

        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_1"
        assert_pdf_upload(route.calls.last.request)
        assert dict(route.calls.last.request.url.params) == {"vendor_tax_id": "BE1018265814"}
        assert_pdf_result(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create_from_pdf(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/documents/pdf").mock(return_value=httpx.Response(200, json=PDF_RESULT_PAYLOAD))

        with client.documents.with_streaming_response.create_from_pdf(
            file=("invoice.pdf", PDF_BYTES, "application/pdf")
        ) as response:
            assert not response.is_closed
            assert_pdf_result(response.parse())

        assert response.is_closed is True
        assert_pdf_upload(route.calls.last.request)

    # send

    @pytest.mark.respx(base_url=base_url)
    def test_send_forwards_peppol_ids_as_query(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/documents/doc_123/send").mock(
            return_value=httpx.Response(200, json=SENT_DOCUMENT_PAYLOAD)
        )

        document = client.documents.send("doc_123", **SEND_PARAMS)

        request = route.calls.last.request
        assert request.method == "POST"
        assert request.url.path == "/api/documents/doc_123/send"
        assert dict(request.url.params) == SEND_PARAMS
        assert request.content == b""
        assert_document(document, state="SENT")

    def test_send_rejects_empty_document_id(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.send("")

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_send(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/documents/doc_123/send").mock(
            return_value=httpx.Response(200, json=SENT_DOCUMENT_PAYLOAD, headers={"x-request-id": "req_1"})
        )

        response = client.documents.with_raw_response.send("doc_123")

        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_1"
        assert route.calls.last.request.url.query == b""
        assert_document(response.parse(), state="SENT")

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_send(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/documents/doc_123/send").mock(
            return_value=httpx.Response(200, json=SENT_DOCUMENT_PAYLOAD)
        )

        with client.documents.with_streaming_response.send("doc_123", receiver_peppol_id="0208:0123456789") as response:
            assert not response.is_closed
            assert_document(response.parse(), state="SENT")

        assert response.is_closed is True
        assert dict(route.calls.last.request.url.params) == {"receiver_peppol_id": "0208:0123456789"}

    # validate

    @pytest.mark.respx(base_url=base_url)
    def test_validate(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/documents/doc_123/validate").mock(
            return_value=httpx.Response(200, json=VALIDATION_PAYLOAD)
        )

        validation = client.documents.validate("doc_123")

        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "POST"
        assert request.url.query == b""
        assert request.content == b""
        assert_validation(validation)

    def test_validate_rejects_empty_document_id(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.validate("")

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_validate(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.post("/api/documents/doc_123/validate").mock(
            return_value=httpx.Response(200, json=VALIDATION_PAYLOAD, headers={"x-request-id": "req_1"})
        )

        response = client.documents.with_raw_response.validate("doc_123")

        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_1"
        assert_validation(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_validate(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.post("/api/documents/doc_123/validate").mock(
            return_value=httpx.Response(200, json=VALIDATION_PAYLOAD)
        )

        with client.documents.with_streaming_response.validate("doc_123") as response:
            assert not response.is_closed
            assert_validation(response.parse())

        assert response.is_closed is True

    # sub-resources

    def test_resource_exposes_wrapper_properties(self, client: EInvoice) -> None:
        raw = client.documents.with_raw_response
        streaming = client.documents.with_streaming_response

        assert isinstance(raw, DocumentsResourceWithRawResponse)
        assert isinstance(streaming, DocumentsResourceWithStreamingResponse)
        assert client.documents.with_raw_response is raw
        assert client.documents.with_streaming_response is streaming

    def test_sub_resources_are_exposed_and_cached(self, client: EInvoice) -> None:
        documents = client.documents

        assert isinstance(documents.attachments, AttachmentsResource)
        assert isinstance(documents.ubl, UblResource)
        assert documents.attachments is documents.attachments
        assert documents.ubl is documents.ubl

        raw = documents.with_raw_response
        assert isinstance(raw.attachments, AttachmentsResourceWithRawResponse)
        assert isinstance(raw.ubl, UblResourceWithRawResponse)
        assert raw.attachments is raw.attachments

        streaming = documents.with_streaming_response
        assert isinstance(streaming.attachments, AttachmentsResourceWithStreamingResponse)
        assert isinstance(streaming.ubl, UblResourceWithStreamingResponse)
        assert streaming.ubl is streaming.ubl


class TestAsyncDocuments:
    # create

    @pytest.mark.respx(base_url=base_url)
    async def test_create_sends_json_body_and_construct_pdf_query(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.post("/api/documents/").mock(return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD))

        document = await async_client.documents.create(construct_pdf=False, **CREATE_PARAMS)

        request = route.calls.last.request
        assert request.method == "POST"
        assert request.url.path == "/api/documents/"
        assert dict(request.url.params) == {"construct_pdf": "false"}
        assert json.loads(request.content) == EXPECTED_CREATE_BODY
        assert_document(document)

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post("/api/documents/").mock(
            return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD, headers={"x-request-id": "req_1"})
        )

        response = await async_client.documents.with_raw_response.create(**CREATE_PARAMS)

        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_1"
        assert json.loads(route.calls.last.request.content) == EXPECTED_CREATE_BODY
        assert_document(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.post("/api/documents/").mock(return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD))

        async with async_client.documents.with_streaming_response.create(**CREATE_PARAMS) as response:
            assert not response.is_closed
            assert_document(await response.parse())

        assert response.is_closed is True

    # retrieve

    @pytest.mark.respx(base_url=base_url)
    async def test_retrieve(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.get("/api/documents/doc_123").mock(return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD))

        document = await async_client.documents.retrieve("doc_123")

        assert route.call_count == 1
        assert route.calls.last.request.method == "GET"
        assert route.calls.last.request.url.query == b""
        assert_document(document)

    async def test_retrieve_rejects_empty_document_id(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.documents.retrieve("")

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/documents/doc_123").mock(
            return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD, headers={"x-request-id": "req_1"})
        )

        response = await async_client.documents.with_raw_response.retrieve("doc_123")

        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_1"
        assert_document(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/documents/doc_123").mock(return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD))

        async with async_client.documents.with_streaming_response.retrieve("doc_123") as response:
            assert not response.is_closed
            assert_document(await response.parse())

        assert response.is_closed is True

    # delete

    @pytest.mark.respx(base_url=base_url)
    async def test_delete(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.delete("/api/documents/doc_123").mock(
            return_value=httpx.Response(200, json={"is_deleted": True})
        )

        result = await async_client.documents.delete("doc_123")

        assert route.call_count == 1
        assert route.calls.last.request.method == "DELETE"
        assert isinstance(result, DocumentDeleteResponse)
        assert result.is_deleted is True

    async def test_delete_rejects_empty_document_id(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.documents.delete("")

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.delete("/api/documents/doc_123").mock(
            return_value=httpx.Response(200, json={"is_deleted": False}, headers={"x-request-id": "req_1"})
        )

        response = await async_client.documents.with_raw_response.delete("doc_123")

        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_1"
        result = await response.parse()
        assert isinstance(result, DocumentDeleteResponse)
        assert result.is_deleted is False

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.delete("/api/documents/doc_123").mock(return_value=httpx.Response(200, json={"is_deleted": True}))

        async with async_client.documents.with_streaming_response.delete("doc_123") as response:
            assert not response.is_closed
            result = await response.parse()
            assert isinstance(result, DocumentDeleteResponse)
            assert result.is_deleted is True

        assert response.is_closed is True

    # create_from_pdf

    @pytest.mark.respx(base_url=base_url)
    async def test_create_from_pdf_uploads_multipart_with_tax_id_query(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.post("/api/documents/pdf").mock(return_value=httpx.Response(200, json=PDF_RESULT_PAYLOAD))

        result = await async_client.documents.create_from_pdf(
            file=("invoice.pdf", PDF_BYTES, "application/pdf"),
            customer_tax_id="NL123456789B01",
            vendor_tax_id="BE1018265814",
        )

        request = route.calls.last.request
        assert_pdf_upload(request)
        assert dict(request.url.params) == {"customer_tax_id": "NL123456789B01", "vendor_tax_id": "BE1018265814"}
        assert_pdf_result(result)

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create_from_pdf(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post("/api/documents/pdf").mock(
            return_value=httpx.Response(200, json=PDF_RESULT_PAYLOAD, headers={"x-request-id": "req_1"})
        )

        response = await async_client.documents.with_raw_response.create_from_pdf(
            file=("invoice.pdf", PDF_BYTES, "application/pdf"), customer_tax_id="NL123456789B01"
        )

        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_1"
        assert_pdf_upload(route.calls.last.request)
        assert dict(route.calls.last.request.url.params) == {"customer_tax_id": "NL123456789B01"}
        assert_pdf_result(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create_from_pdf(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.post("/api/documents/pdf").mock(return_value=httpx.Response(200, json=PDF_RESULT_PAYLOAD))

        async with async_client.documents.with_streaming_response.create_from_pdf(
            file=("invoice.pdf", PDF_BYTES, "application/pdf")
        ) as response:
            assert not response.is_closed
            assert_pdf_result(await response.parse())

        assert response.is_closed is True
        assert_pdf_upload(route.calls.last.request)
        assert route.calls.last.request.url.query == b""

    # send

    @pytest.mark.respx(base_url=base_url)
    async def test_send_forwards_peppol_ids_as_query(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post("/api/documents/doc_123/send").mock(
            return_value=httpx.Response(200, json=SENT_DOCUMENT_PAYLOAD)
        )

        document = await async_client.documents.send("doc_123", email="billing@example.com", **SEND_PARAMS)

        request = route.calls.last.request
        assert request.method == "POST"
        assert request.url.path == "/api/documents/doc_123/send"
        assert dict(request.url.params) == {**SEND_PARAMS, "email": "billing@example.com"}
        assert request.content == b""
        assert_document(document, state="SENT")

    async def test_send_rejects_empty_document_id(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.documents.send("")

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_send(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post("/api/documents/doc_123/send").mock(
            return_value=httpx.Response(200, json=SENT_DOCUMENT_PAYLOAD, headers={"x-request-id": "req_1"})
        )

        response = await async_client.documents.with_raw_response.send("doc_123")

        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_1"
        assert route.calls.last.request.url.query == b""
        assert_document(await response.parse(), state="SENT")

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_send(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post("/api/documents/doc_123/send").mock(
            return_value=httpx.Response(200, json=SENT_DOCUMENT_PAYLOAD)
        )

        async with async_client.documents.with_streaming_response.send(
            "doc_123", sender_peppol_id="0208:1018265814"
        ) as response:
            assert not response.is_closed
            assert_document(await response.parse(), state="SENT")

        assert response.is_closed is True
        assert dict(route.calls.last.request.url.params) == {"sender_peppol_id": "0208:1018265814"}

    # validate

    @pytest.mark.respx(base_url=base_url)
    async def test_validate(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post("/api/documents/doc_123/validate").mock(
            return_value=httpx.Response(200, json=VALIDATION_PAYLOAD)
        )

        validation = await async_client.documents.validate("doc_123")

        assert route.call_count == 1
        assert route.calls.last.request.method == "POST"
        assert route.calls.last.request.content == b""
        assert_validation(validation)

    async def test_validate_rejects_empty_document_id(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.documents.validate("")

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_validate(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.post("/api/documents/doc_123/validate").mock(
            return_value=httpx.Response(200, json=VALIDATION_PAYLOAD, headers={"x-request-id": "req_1"})
        )

        response = await async_client.documents.with_raw_response.validate("doc_123")

        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_1"
        assert_validation(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_validate(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.post("/api/documents/doc_123/validate").mock(
            return_value=httpx.Response(200, json=VALIDATION_PAYLOAD)
        )

        async with async_client.documents.with_streaming_response.validate("doc_123") as response:
            assert not response.is_closed
            assert_validation(await response.parse())

        assert response.is_closed is True

    # sub-resources

    def test_resource_exposes_wrapper_properties(self, async_client: AsyncEInvoice) -> None:
        raw = async_client.documents.with_raw_response
        streaming = async_client.documents.with_streaming_response

        assert isinstance(raw, AsyncDocumentsResourceWithRawResponse)
        assert isinstance(streaming, AsyncDocumentsResourceWithStreamingResponse)
        assert async_client.documents.with_raw_response is raw
        assert async_client.documents.with_streaming_response is streaming

    async def test_sub_resources_are_exposed_and_cached(self, async_client: AsyncEInvoice) -> None:
        documents = async_client.documents

        assert isinstance(documents.attachments, AsyncAttachmentsResource)
        assert isinstance(documents.ubl, AsyncUblResource)
        assert documents.attachments is documents.attachments
        assert documents.ubl is documents.ubl

        raw = documents.with_raw_response
        assert isinstance(raw.attachments, AsyncAttachmentsResourceWithRawResponse)
        assert isinstance(raw.ubl, AsyncUblResourceWithRawResponse)
        assert raw.attachments is raw.attachments

        streaming = documents.with_streaming_response
        assert isinstance(streaming.attachments, AsyncAttachmentsResourceWithStreamingResponse)
        assert isinstance(streaming.ubl, AsyncUblResourceWithStreamingResponse)
        assert streaming.ubl is streaming.ubl
