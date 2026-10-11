from __future__ import annotations

import os
from datetime import date

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import ConversionPdfTask, DocumentCreateFromPdfResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

PDF_BYTES = b"%PDF-1.7 fake invoice body"

RESULT_PAYLOAD = {
    "document_type": "CREDIT_NOTE",
    "state": "DRAFT",
    "direction": "INBOUND",
    "currency": "EUR",
    "tax_code": "S",
    "vatex": None,
    "invoice_id": "INV-2026-001",
    "invoice_date": "2026-02-03",
    "due_date": None,
    "vendor_name": "Acme BV",
    "vendor_tax_id": "BE1018265814",
    "customer_peppol_id": "0208:0123456789",
    "subtotal": "100.00",
    "total_tax": "21.00",
    "invoice_total": "121.00",
    "items": [
        {
            "description": "Consulting",
            "quantity": "2",
            "unit": "C62",
            "unit_price": "50.00",
            "amount": "100.00",
            "tax_rate": "21.00",
            "item_attributes": [{"name": "colour", "value": "blue"}],
        }
    ],
    "tax_details": [{"rate": "21.00", "amount": "21.00"}],
    "payment_details": [{"iban": "BE68539007547034", "payment_reference": "+++123/4567/89012+++"}],
    "success": True,
    "error_message": None,
    "ubl_document": "<Invoice/>",
}


class TestConversion:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_create_pdf_uploads_file_as_multipart(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/conversion/pdf").mock(
            return_value=httpx.Response(201, json={"task_id": "task_abc", "status": "pending"})
        )

        task = client.conversion.create_pdf(file=("invoice.pdf", PDF_BYTES, "application/pdf"))

        request = route.calls.last.request
        assert request.method == "POST"
        assert request.url.path == "/api/conversion/pdf"
        assert request.headers["content-type"].startswith("multipart/form-data; boundary=")
        body = request.read()
        assert b'Content-Disposition: form-data; name="file"; filename="invoice.pdf"' in body
        assert b"Content-Type: application/pdf" in body
        assert PDF_BYTES in body
        assert isinstance(task, ConversionPdfTask)
        assert task.task_id == "task_abc"
        assert task.status == "pending"

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_create_pdf_defaults_missing_status(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.post("/api/conversion/pdf").mock(return_value=httpx.Response(201, json={"task_id": "task_abc"}))

        task = client.conversion.create_pdf(file=PDF_BYTES)

        assert task.task_id == "task_abc"
        assert task.status is None

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_retrieve_pdf_returns_task_status(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/conversion/pdf/task_abc").mock(
            return_value=httpx.Response(200, json={"task_id": "task_abc", "status": "completed"})
        )

        task = client.conversion.retrieve_pdf("task_abc")

        assert route.call_count == 1
        assert route.calls.last.request.method == "GET"
        assert isinstance(task, ConversionPdfTask)
        assert task.task_id == "task_abc"
        assert task.status == "completed"

    @parametrize
    def test_retrieve_pdf_rejects_empty_task_id(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.conversion.retrieve_pdf("")

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_retrieve_pdf_result_parses_converted_document(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/conversion/pdf/task_abc/result").mock(
            return_value=httpx.Response(200, json=RESULT_PAYLOAD)
        )

        result = client.conversion.retrieve_pdf_result("task_abc")

        assert route.call_count == 1
        assert route.calls.last.request.method == "GET"
        assert isinstance(result, DocumentCreateFromPdfResponse)
        assert result.document_type == "CREDIT_NOTE"
        assert result.direction == "INBOUND"
        assert result.invoice_id == "INV-2026-001"
        assert result.invoice_date == date(2026, 2, 3)
        assert result.due_date is None
        assert result.invoice_total == "121.00"
        assert result.success is True
        assert result.ubl_document == "<Invoice/>"
        assert result.items is not None
        assert result.items[0].unit == "C62"
        assert result.items[0].unit_price == "50.00"
        assert result.items[0].item_attributes is not None
        assert result.items[0].item_attributes[0].value == "blue"
        assert result.tax_details is not None
        assert result.tax_details[0].rate == "21.00"
        assert result.payment_details is not None
        assert result.payment_details[0].iban == "BE68539007547034"

    @parametrize
    def test_retrieve_pdf_result_rejects_empty_task_id(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.conversion.retrieve_pdf_result("")

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_raw_response_create_pdf(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.post("/api/conversion/pdf").mock(
            return_value=httpx.Response(201, json={"task_id": "task_raw", "status": "pending"})
        )

        response = client.conversion.with_raw_response.create_pdf(file=PDF_BYTES)

        assert response.is_closed is True
        assert response.status_code == 201
        assert response.http_request.url.path == "/api/conversion/pdf"
        task = response.parse()
        assert isinstance(task, ConversionPdfTask)
        assert task.task_id == "task_raw"

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_raw_response_retrieve_pdf(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/conversion/pdf/task_abc").mock(
            return_value=httpx.Response(200, json={"task_id": "task_abc", "status": "failed"})
        )

        response = client.conversion.with_raw_response.retrieve_pdf("task_abc")

        assert response.is_closed is True
        assert response.http_request.url.path == "/api/conversion/pdf/task_abc"
        assert response.parse().status == "failed"

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_streaming_response_retrieve_pdf_result(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/conversion/pdf/task_abc/result").mock(
            return_value=httpx.Response(200, json=RESULT_PAYLOAD)
        )

        with client.conversion.with_streaming_response.retrieve_pdf_result("task_abc") as response:
            assert not response.is_closed
            result = response.parse()
            assert isinstance(result, DocumentCreateFromPdfResponse)
            assert result.vendor_name == "Acme BV"

        assert response.is_closed is True

    @parametrize
    def test_raw_response_rejects_empty_task_id(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.conversion.with_raw_response.retrieve_pdf("")

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.conversion.with_raw_response.retrieve_pdf_result("")


class TestAsyncConversion:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_create_pdf_uploads_file_as_multipart(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.post("/api/conversion/pdf").mock(
            return_value=httpx.Response(201, json={"task_id": "task_async", "status": "pending"})
        )

        task = await async_client.conversion.create_pdf(file=("invoice.pdf", PDF_BYTES, "application/pdf"))

        request = route.calls.last.request
        assert request.headers["content-type"].startswith("multipart/form-data; boundary=")
        body = request.read()
        assert b'Content-Disposition: form-data; name="file"; filename="invoice.pdf"' in body
        assert PDF_BYTES in body
        assert isinstance(task, ConversionPdfTask)
        assert task.task_id == "task_async"
        assert task.status == "pending"

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_retrieve_pdf_returns_task_status(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.get("/api/conversion/pdf/task_abc").mock(
            return_value=httpx.Response(200, json={"task_id": "task_abc", "status": "completed"})
        )

        task = await async_client.conversion.retrieve_pdf("task_abc")

        assert route.call_count == 1
        assert isinstance(task, ConversionPdfTask)
        assert task.status == "completed"

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_retrieve_pdf_result_parses_converted_document(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.get("/api/conversion/pdf/task_abc/result").mock(
            return_value=httpx.Response(200, json=RESULT_PAYLOAD)
        )

        result = await async_client.conversion.retrieve_pdf_result("task_abc")

        assert route.call_count == 1
        assert isinstance(result, DocumentCreateFromPdfResponse)
        assert result.invoice_date == date(2026, 2, 3)
        assert result.customer_peppol_id == "0208:0123456789"
        assert result.items is not None
        assert result.items[0].amount == "100.00"

    @parametrize
    async def test_rejects_empty_task_id(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.conversion.retrieve_pdf("")

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.conversion.retrieve_pdf_result("")

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_raw_response_retrieve_pdf(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/conversion/pdf/task_abc").mock(
            return_value=httpx.Response(200, json={"task_id": "task_abc", "status": "failed"})
        )

        response = await async_client.conversion.with_raw_response.retrieve_pdf("task_abc")

        assert response.is_closed is True
        assert response.http_request.url.path == "/api/conversion/pdf/task_abc"
        task = await response.parse()
        assert task.status == "failed"

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_streaming_response_create_pdf(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.post("/api/conversion/pdf").mock(
            return_value=httpx.Response(201, json={"task_id": "task_stream", "status": "pending"})
        )

        async with async_client.conversion.with_streaming_response.create_pdf(file=PDF_BYTES) as response:
            assert not response.is_closed
            task = await response.parse()
            assert isinstance(task, ConversionPdfTask)
            assert task.task_id == "task_stream"

        assert response.is_closed is True
