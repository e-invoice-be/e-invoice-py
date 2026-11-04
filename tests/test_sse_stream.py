"""End-to-end tests for the SSE `Stream` and `AsyncStream` classes, driven through the clients.

No endpoint in the SDK streams server-sent events yet, so these call the generic `get` with
`stream=True`, the way a generated streaming method would.
"""

from __future__ import annotations

import os

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, BaseModel, AsyncEInvoice
from e_invoice_api._response import MissingStreamClassError
from e_invoice_api._streaming import Stream, AsyncStream

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

SSE_BODY = (
    b'event: progress\ndata: {"step": 1, "status": "queued"}\n\n'
    b": keep-alive comment\n\n"
    b'event: progress\ndata: {"step": 2, "status": "done"}\n\n'
)


class Event(BaseModel):
    step: int
    status: str


def mock_events(respx_mock: MockRouter, content: bytes = SSE_BODY) -> None:
    respx_mock.get("/events").mock(
        return_value=httpx.Response(200, content=content, headers={"content-type": "text/event-stream"})
    )


class TestStream:
    @pytest.mark.respx(base_url=base_url)
    def test_iterates_parsed_events_and_closes(self, respx_mock: MockRouter, client: EInvoice) -> None:
        mock_events(respx_mock)

        stream = client.get("/events", cast_to=Event, stream=True, stream_cls=Stream[Event])

        assert isinstance(stream, Stream)
        events = list(stream)
        assert events == [Event(step=1, status="queued"), Event(step=2, status="done")]
        assert all(isinstance(event, Event) for event in events)
        assert stream.response.is_closed

    @pytest.mark.respx(base_url=base_url)
    def test_next_yields_one_event_at_a_time(self, respx_mock: MockRouter, client: EInvoice) -> None:
        mock_events(respx_mock)

        stream = client.get("/events", cast_to=Event, stream=True, stream_cls=Stream[Event])

        assert next(stream).step == 1
        assert next(stream).step == 2
        with pytest.raises(StopIteration):
            next(stream)

    @pytest.mark.respx(base_url=base_url)
    def test_context_manager_closes_unread_stream(self, respx_mock: MockRouter, client: EInvoice) -> None:
        mock_events(respx_mock)

        with client.get("/events", cast_to=Event, stream=True, stream_cls=Stream[Event]) as stream:
            assert next(stream).step == 1
            assert not stream.response.is_closed

        assert stream.response.is_closed

    @pytest.mark.respx(base_url=base_url)
    def test_empty_stream_yields_nothing(self, respx_mock: MockRouter, client: EInvoice) -> None:
        mock_events(respx_mock, content=b"")

        stream = client.get("/events", cast_to=Event, stream=True, stream_cls=Stream[Event])

        assert list(stream) == []
        assert stream.response.is_closed

    @pytest.mark.respx(base_url=base_url)
    def test_stream_without_stream_class_raises(self, respx_mock: MockRouter, client: EInvoice) -> None:
        mock_events(respx_mock)

        with pytest.raises(MissingStreamClassError, match=r"`stream_cls` argument was not given"):
            client.get("/events", cast_to=Event, stream=True)


class TestAsyncStream:
    @pytest.mark.respx(base_url=base_url)
    async def test_iterates_parsed_events_and_closes(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        mock_events(respx_mock)

        stream = await async_client.get("/events", cast_to=Event, stream=True, stream_cls=AsyncStream[Event])

        assert isinstance(stream, AsyncStream)
        events = [event async for event in stream]
        assert events == [Event(step=1, status="queued"), Event(step=2, status="done")]
        assert stream.response.is_closed

    @pytest.mark.respx(base_url=base_url)
    async def test_anext_yields_one_event_at_a_time(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        mock_events(respx_mock)

        stream = await async_client.get("/events", cast_to=Event, stream=True, stream_cls=AsyncStream[Event])

        assert (await stream.__anext__()).step == 1
        assert (await stream.__anext__()).step == 2
        with pytest.raises(StopAsyncIteration):
            await stream.__anext__()

    @pytest.mark.respx(base_url=base_url)
    async def test_context_manager_closes_unread_stream(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        mock_events(respx_mock)

        async with await async_client.get(
            "/events", cast_to=Event, stream=True, stream_cls=AsyncStream[Event]
        ) as stream:
            assert (await stream.__anext__()).step == 1
            assert not stream.response.is_closed

        assert stream.response.is_closed

    @pytest.mark.respx(base_url=base_url)
    async def test_empty_stream_yields_nothing(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        mock_events(respx_mock, content=b"")

        stream = await async_client.get("/events", cast_to=Event, stream=True, stream_cls=AsyncStream[Event])

        assert [event async for event in stream] == []
        assert stream.response.is_closed

    @pytest.mark.respx(base_url=base_url)
    async def test_stream_without_stream_class_raises(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        mock_events(respx_mock)

        with pytest.raises(MissingStreamClassError, match=r"`stream_cls` argument was not given"):
            await async_client.get("/events", cast_to=Event, stream=True)
