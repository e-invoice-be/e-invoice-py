"""Tests for the binary and streamed-binary response helpers, on the sync and async clients.

`client.mailbox.download_attachment` is the endpoint that returns binary content, so it drives
the helpers end to end: `iter_bytes`, `iter_text`, `iter_lines`, `write_to_file` and `stream_to_file`.
"""

from __future__ import annotations

import os
import datetime
from pathlib import Path

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api._response import (
    BinaryAPIResponse,
    StreamAlreadyConsumed,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

ATTACHMENT_PATH = "/api/mailbox/ie_01/attachments/invoice.pdf"
PDF_BYTES = b"%PDF-1.7\n\x00\x01\xff binary body\n" * 64
TEXT_BODY = "line one\nlíne twø\r\nline three"
TEXT_LINES = ["line one", "líne twø", "line three"]


def mock_binary(respx_mock: MockRouter, content: bytes = PDF_BYTES) -> None:
    respx_mock.get(ATTACHMENT_PATH).mock(
        return_value=httpx.Response(200, content=content, headers={"content-type": "application/pdf"})
    )


def mock_text(respx_mock: MockRouter) -> None:
    respx_mock.get(ATTACHMENT_PATH).mock(
        return_value=httpx.Response(
            200, content=TEXT_BODY.encode("utf-8"), headers={"content-type": "text/plain; charset=utf-8"}
        )
    )


class TestBinaryResponse:
    @pytest.mark.respx(base_url=base_url)
    def test_iter_bytes_with_chunk_size(self, respx_mock: MockRouter, client: EInvoice) -> None:
        mock_binary(respx_mock)

        with client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            assert isinstance(response, StreamedBinaryAPIResponse)
            chunks = list(response.iter_bytes(chunk_size=100))

        assert b"".join(chunks) == PDF_BYTES
        assert len(chunks) == -(-len(PDF_BYTES) // 100)
        assert all(len(chunk) == 100 for chunk in chunks[:-1])

    @pytest.mark.respx(base_url=base_url)
    def test_iter_text(self, respx_mock: MockRouter, client: EInvoice) -> None:
        mock_text(respx_mock)

        with client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            text = "".join(response.iter_text())

        assert text == TEXT_BODY

    @pytest.mark.respx(base_url=base_url)
    def test_iter_lines(self, respx_mock: MockRouter, client: EInvoice) -> None:
        mock_text(respx_mock)

        with client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            lines = list(response.iter_lines())

        assert lines == TEXT_LINES

    @pytest.mark.respx(base_url=base_url)
    def test_read_after_iterating_raises_stream_already_consumed(
        self, respx_mock: MockRouter, client: EInvoice
    ) -> None:
        mock_binary(respx_mock)

        with client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            for _ in response.iter_bytes():
                pass

            with pytest.raises(StreamAlreadyConsumed, match=r"already been streamed"):
                response.read()

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_context_closes_response(self, respx_mock: MockRouter, client: EInvoice) -> None:
        mock_binary(respx_mock)

        with client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            assert response.is_closed is False

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    def test_response_metadata(self, respx_mock: MockRouter, client: EInvoice) -> None:
        mock_binary(respx_mock)

        response = client.mailbox.download_attachment("invoice.pdf", inbound_email_id="ie_01")

        assert response.method == "GET"
        assert response.url == httpx.URL(base_url + ATTACHMENT_PATH)
        assert response.http_version == "HTTP/1.1"
        assert isinstance(response.elapsed, datetime.timedelta)
        assert response.is_closed is True
        assert repr(response) == "<BinaryAPIResponse [200 OK] type=<class 'bytes'>>"

    @pytest.mark.respx(base_url=base_url)
    def test_write_to_file(self, respx_mock: MockRouter, client: EInvoice, tmp_path: Path) -> None:
        mock_binary(respx_mock)
        target = tmp_path / "invoice.pdf"

        response = client.mailbox.download_attachment("invoice.pdf", inbound_email_id="ie_01")
        assert isinstance(response, BinaryAPIResponse)
        response.write_to_file(target)

        assert target.read_bytes() == PDF_BYTES

    @pytest.mark.respx(base_url=base_url)
    def test_write_to_file_accepts_str_path_and_overwrites(
        self, respx_mock: MockRouter, client: EInvoice, tmp_path: Path
    ) -> None:
        mock_binary(respx_mock, content=b"new")
        target = tmp_path / "invoice.pdf"
        target.write_bytes(b"old content that is longer")

        response = client.mailbox.download_attachment("invoice.pdf", inbound_email_id="ie_01")
        response.write_to_file(str(target))

        assert target.read_bytes() == b"new"

    @pytest.mark.respx(base_url=base_url)
    def test_stream_to_file(self, respx_mock: MockRouter, client: EInvoice, tmp_path: Path) -> None:
        mock_binary(respx_mock)
        target = tmp_path / "invoice.pdf"

        with client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            response.stream_to_file(target, chunk_size=7)

        assert target.read_bytes() == PDF_BYTES

    @pytest.mark.respx(base_url=base_url)
    def test_stream_to_file_empty_body(self, respx_mock: MockRouter, client: EInvoice, tmp_path: Path) -> None:
        mock_binary(respx_mock, content=b"")
        target = tmp_path / "empty.pdf"

        with client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            response.stream_to_file(str(target))

        assert target.exists()
        assert target.read_bytes() == b""


class TestAsyncBinaryResponse:
    @pytest.mark.respx(base_url=base_url)
    async def test_response_metadata(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        mock_binary(respx_mock)

        response = await async_client.mailbox.download_attachment("invoice.pdf", inbound_email_id="ie_01")

        assert response.method == "GET"
        assert response.url == httpx.URL(base_url + ATTACHMENT_PATH)
        assert response.http_version == "HTTP/1.1"
        assert isinstance(response.elapsed, datetime.timedelta)
        assert response.is_closed is True
        assert repr(response) == "<AsyncBinaryAPIResponse [200 OK] type=<class 'bytes'>>"

    @pytest.mark.respx(base_url=base_url)
    async def test_iter_bytes_with_chunk_size(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        mock_binary(respx_mock)

        async with async_client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            assert isinstance(response, AsyncStreamedBinaryAPIResponse)
            chunks = [chunk async for chunk in response.iter_bytes(chunk_size=100)]

        assert b"".join(chunks) == PDF_BYTES
        assert len(chunks) == -(-len(PDF_BYTES) // 100)
        assert all(len(chunk) == 100 for chunk in chunks[:-1])

    @pytest.mark.respx(base_url=base_url)
    async def test_iter_text(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        mock_text(respx_mock)

        async with async_client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            text = "".join([chunk async for chunk in response.iter_text()])

        assert text == TEXT_BODY

    @pytest.mark.respx(base_url=base_url)
    async def test_iter_lines(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        mock_text(respx_mock)

        async with async_client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            lines = [line async for line in response.iter_lines()]

        assert lines == TEXT_LINES

    @pytest.mark.respx(base_url=base_url)
    async def test_read_after_iterating_raises_stream_already_consumed(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        mock_binary(respx_mock)

        async with async_client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            async for _ in response.iter_bytes():
                pass

            with pytest.raises(StreamAlreadyConsumed, match=r"already been streamed"):
                await response.read()

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_context_closes_response(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        mock_binary(respx_mock)

        async with async_client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            assert response.is_closed is False

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    async def test_write_to_file(self, respx_mock: MockRouter, async_client: AsyncEInvoice, tmp_path: Path) -> None:
        mock_binary(respx_mock)
        target = tmp_path / "invoice.pdf"

        response = await async_client.mailbox.download_attachment("invoice.pdf", inbound_email_id="ie_01")
        assert isinstance(response, AsyncBinaryAPIResponse)
        await response.write_to_file(target)

        assert target.read_bytes() == PDF_BYTES

    @pytest.mark.respx(base_url=base_url)
    async def test_write_to_file_accepts_str_path_and_overwrites(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice, tmp_path: Path
    ) -> None:
        mock_binary(respx_mock, content=b"new")
        target = tmp_path / "invoice.pdf"
        target.write_bytes(b"old content that is longer")

        response = await async_client.mailbox.download_attachment("invoice.pdf", inbound_email_id="ie_01")
        await response.write_to_file(str(target))

        assert target.read_bytes() == b"new"

    @pytest.mark.respx(base_url=base_url)
    async def test_stream_to_file(self, respx_mock: MockRouter, async_client: AsyncEInvoice, tmp_path: Path) -> None:
        mock_binary(respx_mock)
        target = tmp_path / "invoice.pdf"

        async with async_client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            await response.stream_to_file(target, chunk_size=7)

        assert target.read_bytes() == PDF_BYTES

    @pytest.mark.respx(base_url=base_url)
    async def test_stream_to_file_empty_body(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice, tmp_path: Path
    ) -> None:
        mock_binary(respx_mock, content=b"")
        target = tmp_path / "empty.pdf"

        async with async_client.mailbox.with_streaming_response.download_attachment(
            "invoice.pdf", inbound_email_id="ie_01"
        ) as response:
            await response.stream_to_file(str(target))

        assert target.exists()
        assert target.read_bytes() == b""
