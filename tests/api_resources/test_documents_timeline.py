from __future__ import annotations

import os
from datetime import datetime, timezone

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import DocumentTimeline

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

TIMELINE_PAYLOAD = {
    "document_id": "doc_123",
    "events": [
        {
            "event_type": "document_created",
            "timestamp": "2026-10-01T08:30:00Z",
            "id": "evt_1",
            "details": {"source": "api"},
        },
        {
            "event_type": "send_success",
            "timestamp": "2026-10-01T08:31:15Z",
            "id": None,
            "details": None,
        },
        {
            "event_type": "mlr_received",
            "timestamp": "2026-10-01T09:00:00Z",
        },
    ],
}


def assert_timeline(timeline: DocumentTimeline) -> None:
    assert isinstance(timeline, DocumentTimeline)
    assert timeline.document_id == "doc_123"
    assert [event.event_type for event in timeline.events] == ["document_created", "send_success", "mlr_received"]

    created, sent, mlr = timeline.events
    assert created.timestamp == datetime(2026, 10, 1, 8, 30, tzinfo=timezone.utc)
    assert created.id == "evt_1"
    assert created.details == {"source": "api"}
    assert sent.timestamp == datetime(2026, 10, 1, 8, 31, 15, tzinfo=timezone.utc)
    assert sent.id is None
    assert sent.details is None
    assert mlr.id is None
    assert mlr.details is None


class TestDocumentsTimeline:
    @pytest.mark.respx(base_url=base_url)
    def test_retrieve_timeline(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/documents/doc_123/timeline").mock(
            return_value=httpx.Response(200, json=TIMELINE_PAYLOAD)
        )

        timeline = client.documents.retrieve_timeline("doc_123")

        assert route.call_count == 1
        assert_timeline(timeline)

    def test_retrieve_timeline_rejects_empty_document_id(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.retrieve_timeline("")

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve_timeline(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/documents/doc_123/timeline").mock(
            return_value=httpx.Response(200, json=TIMELINE_PAYLOAD, headers={"X-Request-Id": "req_1"})
        )

        response = client.documents.with_raw_response.retrieve_timeline("doc_123")

        assert response.is_closed is True
        assert response.status_code == 200
        assert response.headers["X-Request-Id"] == "req_1"
        assert response.http_request.method == "GET"
        assert response.http_request.url.path == "/api/documents/doc_123/timeline"
        assert_timeline(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve_timeline(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/documents/doc_123/timeline").mock(return_value=httpx.Response(200, json=TIMELINE_PAYLOAD))

        with client.documents.with_streaming_response.retrieve_timeline("doc_123") as response:
            assert not response.is_closed
            assert response.http_request.url.path == "/api/documents/doc_123/timeline"
            assert_timeline(response.parse())

        assert response.is_closed is True


class TestAsyncDocumentsTimeline:
    parametrize = pytest.mark.parametrize(
        "async_client", [{"http_client": "httpx"}, {"http_client": "aiohttp"}], indirect=True, ids=["httpx", "aiohttp"]
    )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_retrieve_timeline(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.get("/api/documents/doc_123/timeline").mock(
            return_value=httpx.Response(200, json=TIMELINE_PAYLOAD)
        )

        timeline = await async_client.documents.retrieve_timeline("doc_123")

        assert route.call_count == 1
        assert_timeline(timeline)

    @parametrize
    async def test_retrieve_timeline_rejects_empty_document_id(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.documents.retrieve_timeline("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve_timeline(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/documents/doc_123/timeline").mock(
            return_value=httpx.Response(200, json=TIMELINE_PAYLOAD, headers={"X-Request-Id": "req_1"})
        )

        response = await async_client.documents.with_raw_response.retrieve_timeline("doc_123")

        assert response.is_closed is True
        assert response.status_code == 200
        assert response.headers["X-Request-Id"] == "req_1"
        assert response.http_request.method == "GET"
        assert response.http_request.url.path == "/api/documents/doc_123/timeline"
        assert_timeline(await response.parse())

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve_timeline(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        respx_mock.get("/api/documents/doc_123/timeline").mock(return_value=httpx.Response(200, json=TIMELINE_PAYLOAD))

        async with async_client.documents.with_streaming_response.retrieve_timeline("doc_123") as response:
            assert not response.is_closed
            assert response.http_request.url.path == "/api/documents/doc_123/timeline"
            assert_timeline(await response.parse())

        assert response.is_closed is True
