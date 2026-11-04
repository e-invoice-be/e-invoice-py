from __future__ import annotations

import os
from datetime import datetime, timezone

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import MeRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

ME_PAYLOAD = {
    "name": "Acme",
    "bcc_recipient_email": "archive@acme.example",
    "company_address": "Kerkstraat 1",
    "company_city": "Gent",
    "company_country": "BE",
    "company_email": "billing@acme.example",
    "company_name": "Acme BV",
    "company_number": "1018265814",
    "company_tax_id": "BE1018265814",
    "company_zip": "9000",
    "credit_balance": 250,
    "description": "Test tenant",
    "ibans": ["BE68539007547034"],
    "peppol_ids": ["0208:1018265814", "9925:BE1018265814"],
    "plan": "pro",
    "smp_registration": True,
    "smp_registration_date": "2026-01-15T10:30:00Z",
}


def _assert_full_tenant(me: MeRetrieveResponse) -> None:
    assert isinstance(me, MeRetrieveResponse)
    assert me.name == "Acme"
    assert me.company_name == "Acme BV"
    assert me.company_tax_id == "BE1018265814"
    assert me.credit_balance == 250
    assert me.ibans == ["BE68539007547034"]
    assert me.peppol_ids == ["0208:1018265814", "9925:BE1018265814"]
    assert me.plan == "pro"
    assert me.smp_registration is True
    assert me.smp_registration_date == datetime(2026, 1, 15, 10, 30, tzinfo=timezone.utc)


class TestMe:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_retrieve_parses_tenant(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/me/").mock(return_value=httpx.Response(200, json=ME_PAYLOAD))

        me = client.me.retrieve()

        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/me/"
        assert request.url.query == b""
        _assert_full_tenant(me)

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_retrieve_defaults_optional_fields(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/me/").mock(return_value=httpx.Response(200, json={"name": "Minimal"}))

        me = client.me.retrieve()

        assert me.name == "Minimal"
        assert me.plan is None
        assert me.peppol_ids is None
        assert me.smp_registration_date is None

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_raw_response_retrieve(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/me/").mock(
            return_value=httpx.Response(200, json=ME_PAYLOAD, headers={"x-request-id": "req_me"})
        )

        response = client.me.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.status_code == 200
        assert response.headers["x-request-id"] == "req_me"
        assert response.http_request.url.path == "/api/me/"
        _assert_full_tenant(response.parse())

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_streaming_response_retrieve(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/me/").mock(return_value=httpx.Response(200, json=ME_PAYLOAD))

        with client.me.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            _assert_full_tenant(response.parse())

        assert response.is_closed is True


class TestAsyncMe:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_retrieve_parses_tenant(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.get("/api/me/").mock(return_value=httpx.Response(200, json=ME_PAYLOAD))

        me = await async_client.me.retrieve()

        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/me/"
        assert request.url.query == b""
        _assert_full_tenant(me)

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_raw_response_retrieve(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/me/").mock(return_value=httpx.Response(200, json=ME_PAYLOAD))

        response = await async_client.me.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.url.path == "/api/me/"
        _assert_full_tenant(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_streaming_response_retrieve(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/me/").mock(return_value=httpx.Response(200, json=ME_PAYLOAD))

        async with async_client.me.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            _assert_full_tenant(await response.parse())

        assert response.is_closed is True
