from __future__ import annotations

import os
import json

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, AsyncEInvoice, types

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

HISTORY_PAYLOAD = {
    "history": [
        {"event_type": "document.sent", "status_code": 200, "attempt": 1},
        {"event_type": "document.received", "status_code": 500, "error": {"reason": "timeout"}},
    ]
}


def assert_history(history: types.WebhookRetrieveHistoryResponse) -> None:
    assert isinstance(history, types.WebhookRetrieveHistoryResponse)
    assert history.history == [
        {"event_type": "document.sent", "status_code": 200, "attempt": 1},
        {"event_type": "document.received", "status_code": 500, "error": {"reason": "timeout"}},
    ]


class TestWebhooksHistory:
    @pytest.mark.respx(base_url=base_url)
    def test_retrieve_history(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/webhooks/wh_123/history").mock(
            return_value=httpx.Response(200, json=HISTORY_PAYLOAD)
        )

        history = client.webhooks.retrieve_history("wh_123")

        assert route.call_count == 1
        assert_history(history)

    def test_retrieve_history_rejects_empty_webhook_id(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            client.webhooks.retrieve_history("")

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve_history(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/webhooks/wh_123/history").mock(return_value=httpx.Response(200, json=HISTORY_PAYLOAD))

        response = client.webhooks.with_raw_response.retrieve_history("wh_123")

        assert response.is_closed is True
        assert response.status_code == 200
        assert response.http_request.method == "GET"
        assert response.http_request.url.path == "/api/webhooks/wh_123/history"
        assert_history(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve_history(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/webhooks/wh_123/history").mock(return_value=httpx.Response(200, json=HISTORY_PAYLOAD))

        with client.webhooks.with_streaming_response.retrieve_history("wh_123") as response:
            assert not response.is_closed
            assert response.http_request.url.path == "/api/webhooks/wh_123/history"
            assert_history(response.parse())

        assert response.is_closed is True


TEST_RESPONSE_PAYLOAD = {
    "success": True,
    "message": "Test event delivered",
    "webhook_delivery_result": {"status_code": 200, "duration_ms": 42, "response": {"ok": True}},
}


def assert_test_response(result: types.WebhookTestResponse) -> None:
    assert isinstance(result, types.WebhookTestResponse)
    assert result.success is True
    assert result.message == "Test event delivered"
    assert result.webhook_delivery_result == {"status_code": 200, "duration_ms": 42, "response": {"ok": True}}


class TestWebhooksTest:
    @pytest.mark.respx(base_url=base_url)
    def test_test(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/webhooks/wh_123/test").mock(
            return_value=httpx.Response(200, json=TEST_RESPONSE_PAYLOAD)
        )

        result = client.webhooks.test(
            "wh_123",
            event_type="document.received",
            data={"document_id": "doc_123", "nested": {"amount": 12.5}},
        )

        assert route.call_count == 1
        request = route.calls.last.request
        assert request.headers["Content-Type"] == "application/json"
        assert json.loads(request.content) == {
            "event_type": "document.received",
            "data": {"document_id": "doc_123", "nested": {"amount": 12.5}},
        }
        assert_test_response(result)

    def test_test_rejects_empty_webhook_id(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            client.webhooks.test("", event_type="document.received", data={})

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_test(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.post("/api/webhooks/wh_123/test").mock(return_value=httpx.Response(200, json=TEST_RESPONSE_PAYLOAD))

        response = client.webhooks.with_raw_response.test("wh_123", event_type="document.sent", data={"k": "v"})

        assert response.is_closed is True
        assert response.status_code == 200
        assert response.http_request.method == "POST"
        assert response.http_request.url.path == "/api/webhooks/wh_123/test"
        assert json.loads(response.http_request.content) == {"event_type": "document.sent", "data": {"k": "v"}}
        assert_test_response(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_test(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.post("/api/webhooks/wh_123/test").mock(return_value=httpx.Response(200, json=TEST_RESPONSE_PAYLOAD))

        with client.webhooks.with_streaming_response.test(
            "wh_123", event_type="document.sent", data={"k": "v"}
        ) as response:
            assert not response.is_closed
            assert response.http_request.url.path == "/api/webhooks/wh_123/test"
            assert_test_response(response.parse())

        assert response.is_closed is True


async_parametrize = pytest.mark.parametrize(
    "async_client", [{"http_client": "httpx"}, {"http_client": "aiohttp"}], indirect=True, ids=["httpx", "aiohttp"]
)


class TestAsyncWebhooksHistory:
    @async_parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_retrieve_history(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.get("/api/webhooks/wh_123/history").mock(
            return_value=httpx.Response(200, json=HISTORY_PAYLOAD)
        )

        history = await async_client.webhooks.retrieve_history("wh_123")

        assert route.call_count == 1
        assert_history(history)

    @async_parametrize
    async def test_retrieve_history_rejects_empty_webhook_id(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            await async_client.webhooks.retrieve_history("")

    @async_parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve_history(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/webhooks/wh_123/history").mock(return_value=httpx.Response(200, json=HISTORY_PAYLOAD))

        response = await async_client.webhooks.with_raw_response.retrieve_history("wh_123")

        assert response.is_closed is True
        assert response.status_code == 200
        assert response.http_request.method == "GET"
        assert response.http_request.url.path == "/api/webhooks/wh_123/history"
        assert_history(await response.parse())

    @async_parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve_history(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        respx_mock.get("/api/webhooks/wh_123/history").mock(return_value=httpx.Response(200, json=HISTORY_PAYLOAD))

        async with async_client.webhooks.with_streaming_response.retrieve_history("wh_123") as response:
            assert not response.is_closed
            assert response.http_request.url.path == "/api/webhooks/wh_123/history"
            assert_history(await response.parse())

        assert response.is_closed is True


class TestAsyncWebhooksTest:
    @async_parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_test(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post("/api/webhooks/wh_123/test").mock(
            return_value=httpx.Response(200, json=TEST_RESPONSE_PAYLOAD)
        )

        result = await async_client.webhooks.test(
            "wh_123",
            event_type="document.received",
            data={"document_id": "doc_123", "nested": {"amount": 12.5}},
        )

        assert route.call_count == 1
        request = route.calls.last.request
        assert request.headers["Content-Type"] == "application/json"
        assert json.loads(request.content) == {
            "event_type": "document.received",
            "data": {"document_id": "doc_123", "nested": {"amount": 12.5}},
        }
        assert_test_response(result)

    @async_parametrize
    async def test_test_rejects_empty_webhook_id(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            await async_client.webhooks.test("", event_type="document.received", data={})

    @async_parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_test(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.post("/api/webhooks/wh_123/test").mock(return_value=httpx.Response(200, json=TEST_RESPONSE_PAYLOAD))

        response = await async_client.webhooks.with_raw_response.test(
            "wh_123", event_type="document.sent", data={"k": "v"}
        )

        assert response.is_closed is True
        assert response.status_code == 200
        assert response.http_request.method == "POST"
        assert response.http_request.url.path == "/api/webhooks/wh_123/test"
        assert json.loads(response.http_request.content) == {"event_type": "document.sent", "data": {"k": "v"}}
        assert_test_response(await response.parse())

    @async_parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_test(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.post("/api/webhooks/wh_123/test").mock(return_value=httpx.Response(200, json=TEST_RESPONSE_PAYLOAD))

        async with async_client.webhooks.with_streaming_response.test(
            "wh_123", event_type="document.sent", data={"k": "v"}
        ) as response:
            assert not response.is_closed
            assert response.http_request.url.path == "/api/webhooks/wh_123/test"
            assert_test_response(await response.parse())

        assert response.is_closed is True
