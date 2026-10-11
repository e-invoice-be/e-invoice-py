from __future__ import annotations

import os
from datetime import date

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import StatsRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

STATS_PAYLOAD = {
    "tenant_id": "ten_123",
    "period_start": "2026-01-01",
    "period_end": "2026-01-31",
    "aggregation": "WEEK",
    "actions": [
        {"action": "DOCUMENT_SENT", "stat_date": "2026-01-05", "count": 12},
        {"action": "DOCUMENT_RECEIVED", "stat_date": "2026-01-12", "count": 0},
    ],
    "total_days": 31,
    "average_daily_usage": 0.39,
    "budget_estimation_days": 128.5,
}


class TestStats:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_retrieve_parses_usage_statistics(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/stats").mock(return_value=httpx.Response(200, json=STATS_PAYLOAD))

        stats = client.stats.retrieve()

        assert route.call_count == 1
        assert route.calls.last.request.url.query == b""
        assert isinstance(stats, StatsRetrieveResponse)
        assert stats.tenant_id == "ten_123"
        assert stats.period_start == date(2026, 1, 1)
        assert stats.period_end == date(2026, 1, 31)
        assert stats.aggregation == "WEEK"
        assert stats.total_days == 31
        assert stats.average_daily_usage == 0.39
        assert stats.budget_estimation_days == 128.5
        assert [(a.action, a.stat_date, a.count) for a in stats.actions] == [
            ("DOCUMENT_SENT", date(2026, 1, 5), 12),
            ("DOCUMENT_RECEIVED", date(2026, 1, 12), 0),
        ]

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_retrieve_sends_filters_as_query_string(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/stats").mock(return_value=httpx.Response(200, json=STATS_PAYLOAD))

        client.stats.retrieve(start_date=date(2026, 1, 1), end_date="2026-01-31", aggregation="MONTH")

        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/stats"
        assert dict(request.url.params) == {
            "start_date": "2026-01-01",
            "end_date": "2026-01-31",
            "aggregation": "MONTH",
        }

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_retrieve_defaults_optional_budget_estimation(self, respx_mock: MockRouter, client: EInvoice) -> None:
        payload = {k: v for k, v in STATS_PAYLOAD.items() if k != "budget_estimation_days"}
        payload["actions"] = []
        respx_mock.get("/api/stats").mock(return_value=httpx.Response(200, json=payload))

        stats = client.stats.retrieve()

        assert stats.budget_estimation_days is None
        assert stats.actions == []

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_raw_response_retrieve(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/stats").mock(
            return_value=httpx.Response(200, json=STATS_PAYLOAD, headers={"x-request-id": "req_1"})
        )

        response = client.stats.with_raw_response.retrieve(aggregation="WEEK")

        assert response.is_closed is True
        assert response.status_code == 200
        assert response.headers["x-request-id"] == "req_1"
        assert response.http_request.url.params["aggregation"] == "WEEK"
        stats = response.parse()
        assert isinstance(stats, StatsRetrieveResponse)
        assert stats.actions[0].count == 12

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    def test_streaming_response_retrieve(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/stats").mock(return_value=httpx.Response(200, json=STATS_PAYLOAD))

        with client.stats.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            stats = response.parse()
            assert isinstance(stats, StatsRetrieveResponse)
            assert stats.total_days == 31

        assert response.is_closed is True


class TestAsyncStats:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_retrieve_parses_usage_statistics(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.get("/api/stats").mock(return_value=httpx.Response(200, json=STATS_PAYLOAD))

        stats = await async_client.stats.retrieve(
            start_date=date(2026, 1, 1), end_date=date(2026, 1, 31), aggregation="WEEK"
        )

        assert dict(route.calls.last.request.url.params) == {
            "start_date": "2026-01-01",
            "end_date": "2026-01-31",
            "aggregation": "WEEK",
        }
        assert isinstance(stats, StatsRetrieveResponse)
        assert stats.tenant_id == "ten_123"
        assert stats.period_end == date(2026, 1, 31)
        assert stats.aggregation == "WEEK"
        assert stats.budget_estimation_days == 128.5
        assert [(a.action, a.stat_date, a.count) for a in stats.actions] == [
            ("DOCUMENT_SENT", date(2026, 1, 5), 12),
            ("DOCUMENT_RECEIVED", date(2026, 1, 12), 0),
        ]

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_raw_response_retrieve(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/stats").mock(return_value=httpx.Response(200, json=STATS_PAYLOAD))

        response = await async_client.stats.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.url.path == "/api/stats"
        stats = await response.parse()
        assert isinstance(stats, StatsRetrieveResponse)
        assert stats.average_daily_usage == 0.39

    @pytest.mark.respx(base_url=base_url)
    @parametrize
    async def test_streaming_response_retrieve(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/stats").mock(return_value=httpx.Response(200, json=STATS_PAYLOAD))

        async with async_client.stats.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            stats = await response.parse()
            assert isinstance(stats, StatsRetrieveResponse)
            assert stats.total_days == 31

        assert response.is_closed is True
