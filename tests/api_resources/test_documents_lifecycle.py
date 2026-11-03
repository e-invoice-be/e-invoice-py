from __future__ import annotations

import os
from datetime import datetime, timezone

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import DocumentLifecycle

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

LIFECYCLE_PAYLOAD = {
    "document_id": "doc_123",
    "events": [
        {
            "level": "transport",
            "canonical_status": "delivered",
            "native_code": "AP",
            "source": "peppol:mlr",
            "direction": "in",
            "reason_code": None,
            "reason": None,
            "occurred_at": "2026-10-01T08:30:00Z",
        },
        {
            "level": "business",
            "canonical_status": None,
            "native_code": "XX",
            "source": "peppol:imr",
            "direction": "in",
            "reason_code": "NON",
            "reason": "Unknown status",
            "occurred_at": "2026-10-01T09:00:00Z",
        },
        {
            "level": "business",
            "canonical_status": "paid",
            "native_code": None,
            "source": "local",
            "direction": "out",
            "reason_code": None,
            "reason": None,
            "occurred_at": "2026-10-02T10:15:30Z",
        },
    ],
}


def assert_lifecycle(lifecycle: DocumentLifecycle) -> None:
    assert isinstance(lifecycle, DocumentLifecycle)
    assert lifecycle.document_id == "doc_123"
    assert [event.canonical_status for event in lifecycle.events] == ["delivered", None, "paid"]

    mlr, imr, local = lifecycle.events
    assert mlr.level == "transport"
    assert mlr.native_code == "AP"
    assert mlr.source == "peppol:mlr"
    assert mlr.direction == "in"
    assert mlr.reason_code is None
    assert mlr.reason is None
    assert mlr.occurred_at == datetime(2026, 10, 1, 8, 30, tzinfo=timezone.utc)
    assert imr.level == "business"
    assert imr.native_code == "XX"
    assert imr.reason_code == "NON"
    assert imr.reason == "Unknown status"
    assert local.source == "local"
    assert local.direction == "out"
    assert local.native_code is None
    assert local.occurred_at == datetime(2026, 10, 2, 10, 15, 30, tzinfo=timezone.utc)


class TestDocumentsLifecycle:
    @pytest.mark.respx(base_url=base_url)
    def test_retrieve_lifecycle(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/documents/doc_123/lifecycle").mock(
            return_value=httpx.Response(200, json=LIFECYCLE_PAYLOAD)
        )

        lifecycle = client.documents.retrieve_lifecycle("doc_123")

        assert route.call_count == 1
        assert_lifecycle(lifecycle)

    def test_retrieve_lifecycle_rejects_empty_document_id(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.retrieve_lifecycle("")

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve_lifecycle(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/documents/doc_123/lifecycle").mock(
            return_value=httpx.Response(200, json=LIFECYCLE_PAYLOAD, headers={"X-Request-Id": "req_1"})
        )

        response = client.documents.with_raw_response.retrieve_lifecycle("doc_123")

        assert response.is_closed is True
        assert response.status_code == 200
        assert response.headers["X-Request-Id"] == "req_1"
        assert response.http_request.method == "GET"
        assert response.http_request.url.path == "/api/documents/doc_123/lifecycle"
        assert_lifecycle(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve_lifecycle(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/documents/doc_123/lifecycle").mock(
            return_value=httpx.Response(200, json=LIFECYCLE_PAYLOAD)
        )

        with client.documents.with_streaming_response.retrieve_lifecycle("doc_123") as response:
            assert not response.is_closed
            assert response.http_request.url.path == "/api/documents/doc_123/lifecycle"
            assert_lifecycle(response.parse())

        assert response.is_closed is True


class TestAsyncDocumentsLifecycle:
    parametrize = pytest.mark.parametrize(
        "async_client", [{"http_client": "httpx"}, {"http_client": "aiohttp"}], indirect=True, ids=["httpx", "aiohttp"]
    )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_retrieve_lifecycle(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.get("/api/documents/doc_123/lifecycle").mock(
            return_value=httpx.Response(200, json=LIFECYCLE_PAYLOAD)
        )

        lifecycle = await async_client.documents.retrieve_lifecycle("doc_123")

        assert route.call_count == 1
        assert_lifecycle(lifecycle)

    @parametrize
    async def test_retrieve_lifecycle_rejects_empty_document_id(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.documents.retrieve_lifecycle("")

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve_lifecycle(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/documents/doc_123/lifecycle").mock(
            return_value=httpx.Response(200, json=LIFECYCLE_PAYLOAD, headers={"X-Request-Id": "req_1"})
        )

        response = await async_client.documents.with_raw_response.retrieve_lifecycle("doc_123")

        assert response.is_closed is True
        assert response.status_code == 200
        assert response.headers["X-Request-Id"] == "req_1"
        assert response.http_request.method == "GET"
        assert response.http_request.url.path == "/api/documents/doc_123/lifecycle"
        assert_lifecycle(await response.parse())

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve_lifecycle(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        respx_mock.get("/api/documents/doc_123/lifecycle").mock(
            return_value=httpx.Response(200, json=LIFECYCLE_PAYLOAD)
        )

        async with async_client.documents.with_streaming_response.retrieve_lifecycle("doc_123") as response:
            assert not response.is_closed
            assert response.http_request.url.path == "/api/documents/doc_123/lifecycle"
            assert_lifecycle(await response.parse())

        assert response.is_closed is True
