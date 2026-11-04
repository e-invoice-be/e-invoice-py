from __future__ import annotations

import os
import json
from typing import Any, Dict, List

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import WebhookResponse, WebhookDeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

WEBHOOK_PAYLOAD: Dict[str, Any] = {
    "id": "wh_123",
    "events": ["document.received", "document.sent"],
    "secret": "whsec_abc",
    "url": "https://example.com/hooks",
    "enabled": True,
}

WEBHOOK_WITHOUT_ENABLED: Dict[str, Any] = {
    "id": "wh_456",
    "events": [],
    "secret": "whsec_def",
    "url": "https://example.org/other",
}

LIST_PAYLOAD: List[Dict[str, Any]] = [WEBHOOK_PAYLOAD, WEBHOOK_WITHOUT_ENABLED]

DELETE_PAYLOAD: Dict[str, Any] = {"is_deleted": True}


def assert_webhook(webhook: object, payload: Dict[str, Any] = WEBHOOK_PAYLOAD) -> None:
    assert isinstance(webhook, WebhookResponse)
    assert webhook.id == payload["id"]
    assert webhook.events == payload["events"]
    assert webhook.secret == payload["secret"]
    assert webhook.url == payload["url"]
    assert webhook.enabled == payload.get("enabled")


def assert_webhook_list(webhooks: object) -> None:
    assert isinstance(webhooks, list)
    assert len(webhooks) == 2
    assert_webhook(webhooks[0], WEBHOOK_PAYLOAD)
    assert_webhook(webhooks[1], WEBHOOK_WITHOUT_ENABLED)
    assert webhooks[1].enabled is None


def assert_deleted(result: object) -> None:
    assert isinstance(result, WebhookDeleteResponse)
    assert result.is_deleted is True


def assert_request(request: httpx.Request, method: str, path: str, body: Any = None) -> None:
    assert request.method == method
    assert request.url.path == path
    assert request.url.query == b""
    if body is None:
        assert request.content == b""
    else:
        assert request.headers["Content-Type"] == "application/json"
        assert json.loads(request.content) == body


class TestWebhooks:
    @pytest.mark.respx(base_url=base_url)
    def test_create_with_required_params_only(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/webhooks/").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        webhook = client.webhooks.create(events=["document.received"], url="https://example.com/hooks")

        assert route.call_count == 1
        assert_request(
            route.calls.last.request,
            "POST",
            "/api/webhooks/",
            {"events": ["document.received"], "url": "https://example.com/hooks"},
        )
        assert_webhook(webhook)

    @pytest.mark.respx(base_url=base_url)
    def test_create_with_all_params(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post("/api/webhooks/").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        client.webhooks.create(
            events=("document.received", "document.sent"), url="https://example.com/hooks", enabled=False
        )

        assert_request(
            route.calls.last.request,
            "POST",
            "/api/webhooks/",
            {"events": ["document.received", "document.sent"], "url": "https://example.com/hooks", "enabled": False},
        )

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.post("/api/webhooks/").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        response = client.webhooks.with_raw_response.create(events=["document.sent"], url="https://example.com/hooks")

        assert response.is_closed is True
        assert response.status_code == 200
        assert_request(
            response.http_request,
            "POST",
            "/api/webhooks/",
            {"events": ["document.sent"], "url": "https://example.com/hooks"},
        )
        assert_webhook(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.post("/api/webhooks/").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        with client.webhooks.with_streaming_response.create(
            events=["document.sent"], url="https://example.com/hooks", enabled=True
        ) as response:
            assert not response.is_closed
            assert_request(
                response.http_request,
                "POST",
                "/api/webhooks/",
                {"events": ["document.sent"], "url": "https://example.com/hooks", "enabled": True},
            )
            assert_webhook(response.parse())

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    def test_retrieve(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        webhook = client.webhooks.retrieve("wh_123")

        assert route.call_count == 1
        assert_request(route.calls.last.request, "GET", "/api/webhooks/wh_123")
        assert_webhook(webhook)

    @pytest.mark.respx(base_url=base_url)
    def test_retrieve_defaults_enabled_to_none(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/webhooks/wh_456").mock(return_value=httpx.Response(200, json=WEBHOOK_WITHOUT_ENABLED))

        webhook = client.webhooks.retrieve("wh_456")

        assert_webhook(webhook, WEBHOOK_WITHOUT_ENABLED)
        assert webhook.enabled is None

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        response = client.webhooks.with_raw_response.retrieve("wh_123")

        assert response.is_closed is True
        assert response.status_code == 200
        assert_request(response.http_request, "GET", "/api/webhooks/wh_123")
        assert_webhook(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        with client.webhooks.with_streaming_response.retrieve("wh_123") as response:
            assert not response.is_closed
            assert_request(response.http_request, "GET", "/api/webhooks/wh_123")
            assert_webhook(response.parse())

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    def test_update_with_no_params_sends_empty_body(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.put("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        webhook = client.webhooks.update("wh_123")

        assert route.call_count == 1
        assert_request(route.calls.last.request, "PUT", "/api/webhooks/wh_123", {})
        assert_webhook(webhook)

    @pytest.mark.respx(base_url=base_url)
    def test_update_sends_only_given_fields(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.put("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        client.webhooks.update("wh_123", enabled=False)

        assert_request(route.calls.last.request, "PUT", "/api/webhooks/wh_123", {"enabled": False})

    @pytest.mark.respx(base_url=base_url)
    def test_update_with_all_params(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.put("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        client.webhooks.update("wh_123", enabled=True, events=["document.sent"], url="https://example.com/new")

        assert_request(
            route.calls.last.request,
            "PUT",
            "/api/webhooks/wh_123",
            {"enabled": True, "events": ["document.sent"], "url": "https://example.com/new"},
        )

    @pytest.mark.respx(base_url=base_url)
    def test_update_sends_explicit_nulls(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.put("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        client.webhooks.update("wh_123", enabled=None, events=None, url=None)

        assert_request(
            route.calls.last.request,
            "PUT",
            "/api/webhooks/wh_123",
            {"enabled": None, "events": None, "url": None},
        )

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.put("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        response = client.webhooks.with_raw_response.update("wh_123", url="https://example.com/new")

        assert response.is_closed is True
        assert response.status_code == 200
        assert_request(response.http_request, "PUT", "/api/webhooks/wh_123", {"url": "https://example.com/new"})
        assert_webhook(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.put("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        with client.webhooks.with_streaming_response.update("wh_123", events=["document.received"]) as response:
            assert not response.is_closed
            assert_request(response.http_request, "PUT", "/api/webhooks/wh_123", {"events": ["document.received"]})
            assert_webhook(response.parse())

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    def test_list(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/webhooks/").mock(return_value=httpx.Response(200, json=LIST_PAYLOAD))

        webhooks = client.webhooks.list()

        assert route.call_count == 1
        assert_request(route.calls.last.request, "GET", "/api/webhooks/")
        assert_webhook_list(webhooks)

    @pytest.mark.respx(base_url=base_url)
    def test_list_empty(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/webhooks/").mock(return_value=httpx.Response(200, json=[]))

        assert client.webhooks.list() == []

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/webhooks/").mock(return_value=httpx.Response(200, json=LIST_PAYLOAD))

        response = client.webhooks.with_raw_response.list()

        assert response.is_closed is True
        assert response.status_code == 200
        assert_request(response.http_request, "GET", "/api/webhooks/")
        assert_webhook_list(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/webhooks/").mock(return_value=httpx.Response(200, json=LIST_PAYLOAD))

        with client.webhooks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert_request(response.http_request, "GET", "/api/webhooks/")
            assert_webhook_list(response.parse())

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    def test_delete(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.delete("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=DELETE_PAYLOAD))

        result = client.webhooks.delete("wh_123")

        assert route.call_count == 1
        assert_request(route.calls.last.request, "DELETE", "/api/webhooks/wh_123")
        assert_deleted(result)

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.delete("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=DELETE_PAYLOAD))

        response = client.webhooks.with_raw_response.delete("wh_123")

        assert response.is_closed is True
        assert response.status_code == 200
        assert_request(response.http_request, "DELETE", "/api/webhooks/wh_123")
        assert_deleted(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.delete("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=DELETE_PAYLOAD))

        with client.webhooks.with_streaming_response.delete("wh_123") as response:
            assert not response.is_closed
            assert_request(response.http_request, "DELETE", "/api/webhooks/wh_123")
            assert_deleted(response.parse())

        assert response.is_closed is True

    def test_path_params_reject_empty_webhook_id(self, client: EInvoice) -> None:
        match = r"Expected a non-empty value for `webhook_id` but received ''"
        with pytest.raises(ValueError, match=match):
            client.webhooks.retrieve("")
        with pytest.raises(ValueError, match=match):
            client.webhooks.update("", enabled=True)
        with pytest.raises(ValueError, match=match):
            client.webhooks.delete("")


class TestAsyncWebhooks:
    @pytest.mark.respx(base_url=base_url)
    async def test_create_with_required_params_only(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post("/api/webhooks/").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        webhook = await async_client.webhooks.create(events=["document.received"], url="https://example.com/hooks")

        assert route.call_count == 1
        assert_request(
            route.calls.last.request,
            "POST",
            "/api/webhooks/",
            {"events": ["document.received"], "url": "https://example.com/hooks"},
        )
        assert_webhook(webhook)

    @pytest.mark.respx(base_url=base_url)
    async def test_create_with_all_params(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post("/api/webhooks/").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        await async_client.webhooks.create(
            events=("document.received", "document.sent"), url="https://example.com/hooks", enabled=False
        )

        assert_request(
            route.calls.last.request,
            "POST",
            "/api/webhooks/",
            {"events": ["document.received", "document.sent"], "url": "https://example.com/hooks", "enabled": False},
        )

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.post("/api/webhooks/").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        response = await async_client.webhooks.with_raw_response.create(
            events=["document.sent"], url="https://example.com/hooks"
        )

        assert response.is_closed is True
        assert response.status_code == 200
        assert_request(
            response.http_request,
            "POST",
            "/api/webhooks/",
            {"events": ["document.sent"], "url": "https://example.com/hooks"},
        )
        assert_webhook(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.post("/api/webhooks/").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        async with async_client.webhooks.with_streaming_response.create(
            events=["document.sent"], url="https://example.com/hooks", enabled=True
        ) as response:
            assert not response.is_closed
            assert_request(
                response.http_request,
                "POST",
                "/api/webhooks/",
                {"events": ["document.sent"], "url": "https://example.com/hooks", "enabled": True},
            )
            assert_webhook(await response.parse())

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    async def test_retrieve(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.get("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        webhook = await async_client.webhooks.retrieve("wh_123")

        assert route.call_count == 1
        assert_request(route.calls.last.request, "GET", "/api/webhooks/wh_123")
        assert_webhook(webhook)

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        response = await async_client.webhooks.with_raw_response.retrieve("wh_123")

        assert response.is_closed is True
        assert response.status_code == 200
        assert_request(response.http_request, "GET", "/api/webhooks/wh_123")
        assert_webhook(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        async with async_client.webhooks.with_streaming_response.retrieve("wh_123") as response:
            assert not response.is_closed
            assert_request(response.http_request, "GET", "/api/webhooks/wh_123")
            assert_webhook(await response.parse())

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    async def test_update_with_no_params_sends_empty_body(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.put("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        webhook = await async_client.webhooks.update("wh_123")

        assert route.call_count == 1
        assert_request(route.calls.last.request, "PUT", "/api/webhooks/wh_123", {})
        assert_webhook(webhook)

    @pytest.mark.respx(base_url=base_url)
    async def test_update_with_all_params(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.put("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        await async_client.webhooks.update(
            "wh_123", enabled=True, events=["document.sent"], url="https://example.com/new"
        )

        assert_request(
            route.calls.last.request,
            "PUT",
            "/api/webhooks/wh_123",
            {"enabled": True, "events": ["document.sent"], "url": "https://example.com/new"},
        )

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.put("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        response = await async_client.webhooks.with_raw_response.update("wh_123", url="https://example.com/new")

        assert response.is_closed is True
        assert response.status_code == 200
        assert_request(response.http_request, "PUT", "/api/webhooks/wh_123", {"url": "https://example.com/new"})
        assert_webhook(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.put("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=WEBHOOK_PAYLOAD))

        async with async_client.webhooks.with_streaming_response.update(
            "wh_123", events=["document.received"]
        ) as response:
            assert not response.is_closed
            assert_request(response.http_request, "PUT", "/api/webhooks/wh_123", {"events": ["document.received"]})
            assert_webhook(await response.parse())

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    async def test_list(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.get("/api/webhooks/").mock(return_value=httpx.Response(200, json=LIST_PAYLOAD))

        webhooks = await async_client.webhooks.list()

        assert route.call_count == 1
        assert_request(route.calls.last.request, "GET", "/api/webhooks/")
        assert_webhook_list(webhooks)

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/webhooks/").mock(return_value=httpx.Response(200, json=LIST_PAYLOAD))

        response = await async_client.webhooks.with_raw_response.list()

        assert response.is_closed is True
        assert response.status_code == 200
        assert_request(response.http_request, "GET", "/api/webhooks/")
        assert_webhook_list(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/webhooks/").mock(return_value=httpx.Response(200, json=LIST_PAYLOAD))

        async with async_client.webhooks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert_request(response.http_request, "GET", "/api/webhooks/")
            assert_webhook_list(await response.parse())

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    async def test_delete(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.delete("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=DELETE_PAYLOAD))

        result = await async_client.webhooks.delete("wh_123")

        assert route.call_count == 1
        assert_request(route.calls.last.request, "DELETE", "/api/webhooks/wh_123")
        assert_deleted(result)

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.delete("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=DELETE_PAYLOAD))

        response = await async_client.webhooks.with_raw_response.delete("wh_123")

        assert response.is_closed is True
        assert response.status_code == 200
        assert_request(response.http_request, "DELETE", "/api/webhooks/wh_123")
        assert_deleted(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.delete("/api/webhooks/wh_123").mock(return_value=httpx.Response(200, json=DELETE_PAYLOAD))

        async with async_client.webhooks.with_streaming_response.delete("wh_123") as response:
            assert not response.is_closed
            assert_request(response.http_request, "DELETE", "/api/webhooks/wh_123")
            assert_deleted(await response.parse())

        assert response.is_closed is True

    async def test_path_params_reject_empty_webhook_id(self, async_client: AsyncEInvoice) -> None:
        match = r"Expected a non-empty value for `webhook_id` but received ''"
        with pytest.raises(ValueError, match=match):
            await async_client.webhooks.retrieve("")
        with pytest.raises(ValueError, match=match):
            await async_client.webhooks.update("", enabled=True)
        with pytest.raises(ValueError, match=match):
            await async_client.webhooks.delete("")
