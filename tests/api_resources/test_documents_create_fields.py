from __future__ import annotations

import os
import json
from typing import Any, Dict
from datetime import date

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import DocumentResponse, DocumentCreateFromPdfResponse
from e_invoice_api._compat import parse_obj

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

DOCUMENT_PAYLOAD: Dict[str, Any] = {
    "id": "doc_123",
    "created_at": "2026-10-01T08:30:00Z",
    "buyer_reference": "CC-42",
    "customer_phone": "+49 89 7654321",
    "preceding_invoice_date": "2026-09-01",
    "preceding_invoice_id": "INV-2026-099",
    "rounding_amount": "-0.25",
    "sales_order": "SO-7",
    "tax_currency": "SEK",
    "total_tax_in_tax_currency": "231.50",
    "vendor_phone": "+49 30 1234567",
    "items": [
        {
            "date": "2026-09-15",
            "name": "Wireless mouse",
            "price_base_quantity": "100",
            "description": "Ergonomic wireless mouse",
        },
        {"date": None},
    ],
}

NEW_PARAMS: Dict[str, Any] = {
    "buyer_reference": "CC-42",
    "customer_phone": "+49 89 7654321",
    "preceding_invoice_date": date(2026, 9, 1),
    "preceding_invoice_id": "INV-2026-099",
    "rounding_amount": -0.25,
    "sales_order": "SO-7",
    "tax_currency": "SEK",
    "total_tax_in_tax_currency": "231.50",
    "vendor_phone": "+49 30 1234567",
    "items": [
        {
            "date": date(2026, 9, 15),
            "name": "Wireless mouse",
            "price_base_quantity": 100,
            "description": "Ergonomic wireless mouse",
        },
        {"date": "2026-09-16", "price_base_quantity": "1000"},
    ],
}

EXPECTED_BODY: Dict[str, Any] = {
    "buyer_reference": "CC-42",
    "customer_phone": "+49 89 7654321",
    "preceding_invoice_date": "2026-09-01",
    "preceding_invoice_id": "INV-2026-099",
    "rounding_amount": -0.25,
    "sales_order": "SO-7",
    "tax_currency": "SEK",
    "total_tax_in_tax_currency": "231.50",
    "vendor_phone": "+49 30 1234567",
    "items": [
        {
            "date": "2026-09-15",
            "name": "Wireless mouse",
            "price_base_quantity": 100,
            "description": "Ergonomic wireless mouse",
        },
        {"date": "2026-09-16", "price_base_quantity": "1000"},
    ],
}


def assert_document(document: DocumentResponse) -> None:
    assert isinstance(document, DocumentResponse)
    assert document.buyer_reference == "CC-42"
    assert document.customer_phone == "+49 89 7654321"
    assert document.preceding_invoice_date == date(2026, 9, 1)
    assert document.preceding_invoice_id == "INV-2026-099"
    assert document.rounding_amount == "-0.25"
    assert document.sales_order == "SO-7"
    assert document.tax_currency == "SEK"
    assert document.total_tax_in_tax_currency == "231.50"
    assert document.vendor_phone == "+49 30 1234567"
    assert document.items is not None
    first, second = document.items
    assert first.date == date(2026, 9, 15)
    assert first.name == "Wireless mouse"
    assert first.price_base_quantity == "100"
    assert second.date is None
    assert second.name is None
    assert second.price_base_quantity is None


def test_create_from_pdf_response_parses_new_fields() -> None:
    payload = {key: value for key, value in DOCUMENT_PAYLOAD.items() if key not in ("id", "created_at")}

    document = parse_obj(DocumentCreateFromPdfResponse, payload)

    assert document.buyer_reference == "CC-42"
    assert document.preceding_invoice_date == date(2026, 9, 1)
    assert document.rounding_amount == "-0.25"
    assert document.total_tax_in_tax_currency == "231.50"
    assert document.vendor_phone == "+49 30 1234567"
    assert document.items is not None
    first, second = document.items
    assert first.date == date(2026, 9, 15)
    assert first.name == "Wireless mouse"
    assert first.price_base_quantity == "100"
    assert second.date is None


class TestDocumentsCreateFields:
    @pytest.mark.respx(base_url=base_url)
    def test_create_with_new_params(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/documents/").mock(return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD))

        document = client.documents.create(**NEW_PARAMS)

        assert route.call_count == 1
        assert json.loads(route.calls.last.request.content) == EXPECTED_BODY
        assert_document(document)

    @pytest.mark.respx(base_url=base_url)
    def test_validate_json_with_new_params(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/validate/json").mock(
            return_value=httpx.Response(200, json={"id": "doc_123", "is_valid": True, "issues": []})
        )

        client.validate.validate_json(**NEW_PARAMS)

        assert route.call_count == 1
        assert json.loads(route.calls.last.request.content) == EXPECTED_BODY

    @pytest.mark.respx(base_url=base_url)
    def test_send_still_forwards_deprecated_email(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/documents/doc_123/send").mock(
            return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD)
        )

        client.documents.send("doc_123", email="billing@example.com")

        assert route.call_count == 1
        assert route.calls.last.request.url.params["email"] == "billing@example.com"


class TestAsyncDocumentsCreateFields:
    @pytest.mark.respx(base_url=base_url)
    async def test_create_with_new_params(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post("/api/documents/").mock(return_value=httpx.Response(200, json=DOCUMENT_PAYLOAD))

        document = await async_client.documents.create(**NEW_PARAMS)

        assert route.call_count == 1
        assert json.loads(route.calls.last.request.content) == EXPECTED_BODY
        assert_document(document)

    @pytest.mark.respx(base_url=base_url)
    async def test_validate_json_with_new_params(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post("/api/validate/json").mock(
            return_value=httpx.Response(200, json={"id": "doc_123", "is_valid": True, "issues": []})
        )

        await async_client.validate.validate_json(**NEW_PARAMS)

        assert route.call_count == 1
        assert json.loads(route.calls.last.request.content) == EXPECTED_BODY
