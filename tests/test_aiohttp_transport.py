"""End-to-end tests of the aiohttp transport (`DefaultAioHttpClient`).

respx can't mock custom transports, so these tests send real requests to a local
`aiohttp.web` server instead.
"""

from __future__ import annotations

from typing import Callable, Awaitable, AsyncIterator

import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from e_invoice_api import AsyncEInvoice, NotFoundError, DefaultAioHttpClient
from e_invoice_api.types import MeRetrieveResponse

api_key = "My API Key"

PDF_BYTES = b"%PDF-1.7\n" + bytes(range(256)) * 64


async def _me(request: web.Request) -> web.Response:
    return web.json_response(
        {
            "name": "Acme BV",
            "seen_authorization": request.headers.get("Authorization"),
        }
    )


async def _attachment(request: web.Request) -> web.StreamResponse:
    # written in several chunks, so the body arrives over more than one network read
    response = web.StreamResponse(headers={"Content-Type": "application/pdf"})
    await response.prepare(request)
    for start in range(0, len(PDF_BYTES), 4096):
        await response.write(PDF_BYTES[start : start + 4096])
    await response.write_eof()
    return response


async def _not_found(_request: web.Request) -> web.Response:
    return web.json_response({"detail": "Document not found"}, status=404)


def _flaky(state: dict[str, int]) -> Callable[[web.Request], Awaitable[web.Response]]:
    async def handler(_request: web.Request) -> web.Response:
        state["calls"] += 1
        if state["calls"] == 1:
            # retry-after-ms keeps the client's back-off at one millisecond
            return web.json_response({"detail": "try again"}, status=503, headers={"retry-after-ms": "1"})
        return web.json_response({"name": "Acme BV"})

    return handler


@pytest.fixture
def flaky_state() -> dict[str, int]:
    return {"calls": 0}


@pytest.fixture
async def server(flaky_state: dict[str, int]) -> AsyncIterator[TestServer]:
    app = web.Application()
    app.router.add_get("/api/me/", _me)
    app.router.add_get("/api/mailbox/{inbound_email_id}/attachments/{filename}", _attachment)
    app.router.add_get("/api/documents/{document_id}", _not_found)
    app.router.add_get("/api/flaky/", _flaky(flaky_state))

    test_server = TestServer(app)
    await test_server.start_server()
    try:
        yield test_server
    finally:
        await test_server.close()


@pytest.fixture
async def aio_client(server: TestServer) -> AsyncIterator[AsyncEInvoice]:
    async with AsyncEInvoice(
        base_url=str(server.make_url("")),
        api_key=api_key,
        _strict_response_validation=True,
        http_client=DefaultAioHttpClient(),
    ) as client:
        assert isinstance(client._client, DefaultAioHttpClient)
        yield client


class TestAioHttpTransport:
    async def test_json_response_is_parsed(self, aio_client: AsyncEInvoice) -> None:
        me = await aio_client.me.retrieve()

        assert isinstance(me, MeRetrieveResponse)
        assert me.name == "Acme BV"
        assert me.to_dict()["seen_authorization"] == f"Bearer {api_key}"

    async def test_binary_download_reads_the_whole_body(self, aio_client: AsyncEInvoice) -> None:
        response = await aio_client.mailbox.download_attachment("invoice.pdf", inbound_email_id="ie_01")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert await response.read() == PDF_BYTES

    async def test_streaming_response_reads_the_body_lazily(self, aio_client: AsyncEInvoice) -> None:
        async with aio_client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            assert response.http_request.headers["accept"] == "*/*"
            # the streaming wrapper must not have read the body before we iterate it
            assert not response.http_response.is_stream_consumed
            chunks = [chunk async for chunk in response.iter_bytes(1024)]

        assert b"".join(chunks) == PDF_BYTES
        assert len(chunks) > 1
        assert all(len(chunk) == 1024 for chunk in chunks[:-1])

    async def test_error_status_raises_mapped_exception(self, aio_client: AsyncEInvoice) -> None:
        with pytest.raises(NotFoundError) as exc_info:
            await aio_client.with_options(max_retries=0).documents.retrieve("doc_missing")

        assert exc_info.value.status_code == 404
        assert exc_info.value.body == {"detail": "Document not found"}

    async def test_retries_a_server_error(self, aio_client: AsyncEInvoice, flaky_state: dict[str, int]) -> None:
        response = await aio_client.with_options(max_retries=2).get("/api/flaky/", cast_to=MeRetrieveResponse)

        assert flaky_state["calls"] == 2
        assert response.name == "Acme BV"
