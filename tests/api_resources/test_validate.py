from __future__ import annotations

import os
import json
from datetime import date

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import UblDocumentValidation, ValidateValidateJsonParams, ValidateValidatePeppolIDResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

PEPPOL_ID = "0208:1018265814"

UBL_BYTES = b'<?xml version="1.0"?><Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"/>'

VALIDATION_PAYLOAD = {
    "id": "val_123",
    "file_name": "invoice.xml",
    "is_valid": False,
    "issues": [
        {
            "message": "[BR-CO-15] Invoice total amount with VAT = total without VAT + total VAT.",
            "schematron": "CEN-EN16931-UBL",
            "type": "error",
            "flag": "fatal",
            "location": "/Invoice[1]",
            "rule_id": "BR-CO-15",
            "test": "every $Currency in ...",
        },
        {"message": "Buyer reference missing", "schematron": "PEPPOL-EN16931-UBL", "type": "warning"},
    ],
    "ubl_document": "<Invoice/>",
}

PEPPOL_ID_PAYLOAD = {
    "business_card_valid": True,
    "dns_valid": True,
    "is_valid": True,
    "supported_document_types": ["urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::Invoice"],
    "business_card": {"country_code": "BE", "name": "Acme BV", "registration_date": "2024-03-01"},
}

# The keyword arguments passed to `validate_json`, alongside the JSON body we expect on the wire.
JSON_KWARGS: ValidateValidateJsonParams = {
    "invoice_id": "INV-2026-001",
    "invoice_date": date(2026, 2, 3),
    "due_date": "2026-03-05",
    "currency": "EUR",
    "document_type": "INVOICE",
    "direction": "OUTBOUND",
    "state": "DRAFT",
    "tax_code": "S",
    "vendor_name": "Acme BV",
    "vendor_tax_id": "BE1018265814",
    "customer_name": "Globex NV",
    "customer_peppol_id": "0208:0123456789",
    "subtotal": "100.00",
    "total_tax": 21,
    "invoice_total": "121.00",
    "items": [
        {
            "description": "Consulting",
            "quantity": 2,
            "unit": "C62",
            "unit_price": "50.00",
            "amount": "100.00",
            "tax_rate": "21.00",
            "date": date(2026, 2, 1),
            "item_attributes": [{"name": "colour", "value": "blue"}],
            "allowances": [{"amount": "5.00", "reason": "Loyalty", "tax_code": "S", "tax_rate": "21.00"}],
        }
    ],
    "tax_details": [{"amount": "21.00", "rate": "21.00"}],
    "payment_details": [{"iban": "BE68539007547034", "payment_reference": "+++123/4567/89012+++"}],
}

EXPECTED_JSON_BODY = {
    "invoice_id": "INV-2026-001",
    "invoice_date": "2026-02-03",
    "due_date": "2026-03-05",
    "currency": "EUR",
    "document_type": "INVOICE",
    "direction": "OUTBOUND",
    "state": "DRAFT",
    "tax_code": "S",
    "vendor_name": "Acme BV",
    "vendor_tax_id": "BE1018265814",
    "customer_name": "Globex NV",
    "customer_peppol_id": "0208:0123456789",
    "subtotal": "100.00",
    "total_tax": 21,
    "invoice_total": "121.00",
    "items": [
        {
            "description": "Consulting",
            "quantity": 2,
            "unit": "C62",
            "unit_price": "50.00",
            "amount": "100.00",
            "tax_rate": "21.00",
            "date": "2026-02-01",
            "item_attributes": [{"name": "colour", "value": "blue"}],
            "allowances": [{"amount": "5.00", "reason": "Loyalty", "tax_code": "S", "tax_rate": "21.00"}],
        }
    ],
    "tax_details": [{"amount": "21.00", "rate": "21.00"}],
    "payment_details": [{"iban": "BE68539007547034", "payment_reference": "+++123/4567/89012+++"}],
}


def _assert_validation(result: UblDocumentValidation) -> None:
    assert isinstance(result, UblDocumentValidation)
    assert result.id == "val_123"
    assert result.file_name == "invoice.xml"
    assert result.is_valid is False
    assert result.ubl_document == "<Invoice/>"
    assert [(i.type, i.rule_id, i.flag) for i in result.issues] == [
        ("error", "BR-CO-15", "fatal"),
        ("warning", None, None),
    ]
    assert result.issues[1].schematron == "PEPPOL-EN16931-UBL"


def _assert_peppol_id(result: ValidateValidatePeppolIDResponse) -> None:
    assert isinstance(result, ValidateValidatePeppolIDResponse)
    assert result.is_valid is True
    assert result.dns_valid is True
    assert result.business_card_valid is True
    assert result.supported_document_types == ["urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::Invoice"]
    assert result.business_card is not None
    assert result.business_card.name == "Acme BV"
    assert result.business_card.registration_date == date(2024, 3, 1)


def _assert_json_request(request: httpx.Request) -> None:
    assert request.method == "POST"
    assert request.url.path == "/api/validate/json"
    assert request.headers["content-type"] == "application/json"
    assert json.loads(request.content) == EXPECTED_JSON_BODY


def _assert_multipart_request(request: httpx.Request) -> None:
    assert request.method == "POST"
    assert request.url.path == "/api/validate/ubl"
    assert request.headers["content-type"].startswith("multipart/form-data; boundary=")
    body = request.read()
    assert b'Content-Disposition: form-data; name="file"; filename="invoice.xml"' in body
    assert b"Content-Type: application/xml" in body
    assert UBL_BYTES in body


class TestValidate:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_validate_json_sends_document_as_json(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/validate/json").mock(return_value=httpx.Response(200, json=VALIDATION_PAYLOAD))

        result = client.validate.validate_json(**JSON_KWARGS)

        assert route.call_count == 1
        _assert_json_request(route.calls.last.request)
        _assert_validation(result)

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_validate_json_without_params_sends_empty_object(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/validate/json").mock(
            return_value=httpx.Response(200, json={"id": "val_empty", "is_valid": True, "issues": []})
        )

        result = client.validate.validate_json()

        assert json.loads(route.calls.last.request.content) == {}
        assert result.is_valid is True
        assert result.issues == []
        assert result.file_name is None
        assert result.ubl_document is None

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_raw_response_validate_json(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.post("/api/validate/json").mock(
            return_value=httpx.Response(200, json=VALIDATION_PAYLOAD, headers={"x-request-id": "req_json"})
        )

        response = client.validate.with_raw_response.validate_json(**JSON_KWARGS)

        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_json"
        _assert_json_request(response.http_request)
        _assert_validation(response.parse())

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_streaming_response_validate_json(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/validate/json").mock(return_value=httpx.Response(200, json=VALIDATION_PAYLOAD))

        with client.validate.with_streaming_response.validate_json(**JSON_KWARGS) as response:
            assert not response.is_closed
            _assert_validation(response.parse())

        assert response.is_closed is True
        _assert_json_request(route.calls.last.request)

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_validate_peppol_id_sends_query(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/validate/peppol-id").mock(return_value=httpx.Response(200, json=PEPPOL_ID_PAYLOAD))

        result = client.validate.validate_peppol_id(peppol_id=PEPPOL_ID)

        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/validate/peppol-id"
        assert dict(request.url.params) == {"peppol_id": PEPPOL_ID}
        _assert_peppol_id(result)

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_validate_peppol_id_unknown_participant(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/validate/peppol-id").mock(
            return_value=httpx.Response(
                200,
                json={
                    "business_card_valid": False,
                    "dns_valid": False,
                    "is_valid": False,
                    "supported_document_types": [],
                },
            )
        )

        result = client.validate.validate_peppol_id(peppol_id="0208:0000000000")

        assert result.is_valid is False
        assert result.supported_document_types == []
        assert result.business_card is None

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_raw_response_validate_peppol_id(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/validate/peppol-id").mock(return_value=httpx.Response(200, json=PEPPOL_ID_PAYLOAD))

        response = client.validate.with_raw_response.validate_peppol_id(peppol_id=PEPPOL_ID)

        assert response.is_closed is True
        assert response.status_code == 200
        assert response.http_request.url.params["peppol_id"] == PEPPOL_ID
        _assert_peppol_id(response.parse())

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_streaming_response_validate_peppol_id(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/validate/peppol-id").mock(return_value=httpx.Response(200, json=PEPPOL_ID_PAYLOAD))

        with client.validate.with_streaming_response.validate_peppol_id(peppol_id=PEPPOL_ID) as response:
            assert not response.is_closed
            _assert_peppol_id(response.parse())

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_validate_ubl_uploads_file_as_multipart(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/validate/ubl").mock(return_value=httpx.Response(200, json=VALIDATION_PAYLOAD))

        result = client.validate.validate_ubl(file=("invoice.xml", UBL_BYTES, "application/xml"))

        assert route.call_count == 1
        _assert_multipart_request(route.calls.last.request)
        _assert_validation(result)

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_raw_response_validate_ubl(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.post("/api/validate/ubl").mock(return_value=httpx.Response(200, json=VALIDATION_PAYLOAD))

        response = client.validate.with_raw_response.validate_ubl(file=("invoice.xml", UBL_BYTES, "application/xml"))

        assert response.is_closed is True
        _assert_multipart_request(response.http_request)
        _assert_validation(response.parse())

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_streaming_response_validate_ubl(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/validate/ubl").mock(return_value=httpx.Response(200, json=VALIDATION_PAYLOAD))

        with client.validate.with_streaming_response.validate_ubl(
            file=("invoice.xml", UBL_BYTES, "application/xml")
        ) as response:
            assert not response.is_closed
            _assert_validation(response.parse())

        assert response.is_closed is True
        _assert_multipart_request(route.calls.last.request)


class TestAsyncValidate:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_validate_json_sends_document_as_json(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.post("/api/validate/json").mock(return_value=httpx.Response(200, json=VALIDATION_PAYLOAD))

        result = await async_client.validate.validate_json(**JSON_KWARGS)

        _assert_json_request(route.calls.last.request)
        _assert_validation(result)

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_raw_response_validate_json(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.post("/api/validate/json").mock(return_value=httpx.Response(200, json=VALIDATION_PAYLOAD))

        response = await async_client.validate.with_raw_response.validate_json(**JSON_KWARGS)

        assert response.is_closed is True
        _assert_json_request(response.http_request)
        _assert_validation(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_streaming_response_validate_json(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post("/api/validate/json").mock(return_value=httpx.Response(200, json=VALIDATION_PAYLOAD))

        async with async_client.validate.with_streaming_response.validate_json(**JSON_KWARGS) as response:
            assert not response.is_closed
            _assert_validation(await response.parse())

        assert response.is_closed is True
        _assert_json_request(route.calls.last.request)

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_validate_peppol_id_sends_query(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.get("/api/validate/peppol-id").mock(return_value=httpx.Response(200, json=PEPPOL_ID_PAYLOAD))

        result = await async_client.validate.validate_peppol_id(peppol_id=PEPPOL_ID)

        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/validate/peppol-id"
        assert dict(request.url.params) == {"peppol_id": PEPPOL_ID}
        _assert_peppol_id(result)

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_raw_response_validate_peppol_id(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/validate/peppol-id").mock(return_value=httpx.Response(200, json=PEPPOL_ID_PAYLOAD))

        response = await async_client.validate.with_raw_response.validate_peppol_id(peppol_id=PEPPOL_ID)

        assert response.is_closed is True
        assert response.http_request.url.params["peppol_id"] == PEPPOL_ID
        _assert_peppol_id(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_streaming_response_validate_peppol_id(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        respx_mock.get("/api/validate/peppol-id").mock(return_value=httpx.Response(200, json=PEPPOL_ID_PAYLOAD))

        async with async_client.validate.with_streaming_response.validate_peppol_id(peppol_id=PEPPOL_ID) as response:
            assert not response.is_closed
            _assert_peppol_id(await response.parse())

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_validate_ubl_uploads_file_as_multipart(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.post("/api/validate/ubl").mock(return_value=httpx.Response(200, json=VALIDATION_PAYLOAD))

        result = await async_client.validate.validate_ubl(file=("invoice.xml", UBL_BYTES, "application/xml"))

        _assert_multipart_request(route.calls.last.request)
        _assert_validation(result)

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_raw_response_validate_ubl(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.post("/api/validate/ubl").mock(return_value=httpx.Response(200, json=VALIDATION_PAYLOAD))

        response = await async_client.validate.with_raw_response.validate_ubl(
            file=("invoice.xml", UBL_BYTES, "application/xml")
        )

        assert response.is_closed is True
        _assert_multipart_request(response.http_request)
        _assert_validation(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_streaming_response_validate_ubl(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post("/api/validate/ubl").mock(return_value=httpx.Response(200, json=VALIDATION_PAYLOAD))

        async with async_client.validate.with_streaming_response.validate_ubl(
            file=("invoice.xml", UBL_BYTES, "application/xml")
        ) as response:
            assert not response.is_closed
            _assert_validation(await response.parse())

        assert response.is_closed is True
        _assert_multipart_request(route.calls.last.request)
