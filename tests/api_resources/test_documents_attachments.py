from __future__ import annotations

import os
from typing import Any, Dict, List
from contextlib import ExitStack

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, AsyncEInvoice, NotFoundError
from e_invoice_api._response import APIResponse, AsyncAPIResponse
from e_invoice_api.types.documents import DocumentAttachment, AttachmentDeleteResponse
from e_invoice_api.resources.documents.attachments import (
    AttachmentsResourceWithRawResponse,
    AsyncAttachmentsResourceWithRawResponse,
    AttachmentsResourceWithStreamingResponse,
    AsyncAttachmentsResourceWithStreamingResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

PDF_BYTES = b"%PDF-1.7\n\x00\x01\xff signed delivery note"

FULL_ATTACHMENT: Dict[str, Any] = {
    "id": "att_01",
    "file_name": "delivery-note.pdf",
    "file_size": 2048,
    "file_type": "application/pdf",
    "file_url": "https://storage.example.com/att_01?signature=abc&expires=3600",
}

MINIMAL_ATTACHMENT: Dict[str, Any] = {
    "id": "att_02",
    "file_name": "timesheet.csv",
}

ATTACHMENTS_PATH = "/api/documents/doc_123/attachments"
ATTACHMENT_PATH = "/api/documents/doc_123/attachments/att_01"


def assert_full_attachment(attachment: object) -> None:
    assert isinstance(attachment, DocumentAttachment)
    assert attachment.id == "att_01"
    assert attachment.file_name == "delivery-note.pdf"
    assert attachment.file_size == 2048
    assert attachment.file_type == "application/pdf"
    assert attachment.file_url == "https://storage.example.com/att_01?signature=abc&expires=3600"


def assert_attachment_list(attachments: object) -> None:
    assert isinstance(attachments, list)
    items: List[Any] = attachments
    assert all(isinstance(item, DocumentAttachment) for item in items)
    assert [item.id for item in items] == ["att_01", "att_02"]
    minimal = items[1]
    assert minimal.file_name == "timesheet.csv"
    assert minimal.file_size is None
    assert minimal.file_type is None
    assert minimal.file_url is None


def assert_multipart_upload(request: httpx.Request) -> None:
    assert request.method == "POST"
    assert request.url.path == ATTACHMENTS_PATH
    assert request.url.query == b""
    assert request.headers["content-type"].startswith("multipart/form-data; boundary=")
    body = request.read()
    assert b'Content-Disposition: form-data; name="file"; filename="delivery-note.pdf"' in body
    assert b"Content-Type: application/pdf" in body
    assert PDF_BYTES in body


class TestAttachments:
    def test_resource_exposes_wrapper_properties(self, client: EInvoice) -> None:
        raw = client.documents.attachments.with_raw_response
        streaming = client.documents.attachments.with_streaming_response

        assert isinstance(raw, AttachmentsResourceWithRawResponse)
        assert isinstance(streaming, AttachmentsResourceWithStreamingResponse)
        # cached_property: repeated access returns the same wrapper
        assert client.documents.attachments.with_raw_response is raw
        assert client.documents.attachments.with_streaming_response is streaming

    @pytest.mark.respx(base_url=base_url)
    def test_retrieve_parses_attachment(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get(ATTACHMENT_PATH).mock(return_value=httpx.Response(200, json=FULL_ATTACHMENT))

        attachment = client.documents.attachments.retrieve("att_01", document_id="doc_123")

        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.query == b""
        assert request.content == b""
        assert_full_attachment(attachment)

    @pytest.mark.respx(base_url=base_url)
    def test_retrieve_escapes_path_params(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get(url__regex=r".*/attachments/.*").mock(
            return_value=httpx.Response(200, json=MINIMAL_ATTACHMENT)
        )

        client.documents.attachments.retrieve("att/02", document_id="doc 123")

        assert route.calls.last.request.url.raw_path == b"/api/documents/doc%20123/attachments/att%2F02"

    def test_retrieve_rejects_empty_path_params(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.attachments.retrieve("att_01", document_id="")

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `attachment_id` but received ''"):
            client.documents.attachments.retrieve("", document_id="doc_123")

    @pytest.mark.respx(base_url=base_url)
    def test_retrieve_not_found_raises(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get(ATTACHMENT_PATH).mock(return_value=httpx.Response(404, json={"detail": "Attachment not found"}))

        with pytest.raises(NotFoundError) as exc_info:
            client.with_options(max_retries=0).documents.attachments.retrieve("att_01", document_id="doc_123")

        assert exc_info.value.status_code == 404

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get(ATTACHMENT_PATH).mock(
            return_value=httpx.Response(200, json=FULL_ATTACHMENT, headers={"x-request-id": "req_1"})
        )

        response = client.documents.attachments.with_raw_response.retrieve("att_01", document_id="doc_123")

        assert isinstance(response, APIResponse)
        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_1"
        assert_full_attachment(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get(ATTACHMENT_PATH).mock(return_value=httpx.Response(200, json=FULL_ATTACHMENT))

        with client.documents.attachments.with_streaming_response.retrieve("att_01", document_id="doc_123") as response:
            assert not response.is_closed
            assert_full_attachment(response.parse())

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    def test_list_returns_plain_list_of_attachments(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get(ATTACHMENTS_PATH).mock(
            return_value=httpx.Response(200, json=[FULL_ATTACHMENT, MINIMAL_ATTACHMENT])
        )

        attachments = client.documents.attachments.list("doc_123")

        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.query == b""
        assert_attachment_list(attachments)
        assert_full_attachment(attachments[0])

    @pytest.mark.respx(base_url=base_url)
    def test_list_empty(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get(ATTACHMENTS_PATH).mock(return_value=httpx.Response(200, json=[]))

        assert client.documents.attachments.list("doc_123") == []

    def test_list_rejects_empty_document_id(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.attachments.list("")

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get(ATTACHMENTS_PATH).mock(
            return_value=httpx.Response(200, json=[FULL_ATTACHMENT, MINIMAL_ATTACHMENT])
        )

        response = client.documents.attachments.with_raw_response.list("doc_123")

        assert response.is_closed is True
        assert response.status_code == 200
        assert_attachment_list(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get(ATTACHMENTS_PATH).mock(
            return_value=httpx.Response(200, json=[FULL_ATTACHMENT, MINIMAL_ATTACHMENT])
        )

        with client.documents.attachments.with_streaming_response.list("doc_123") as response:
            assert not response.is_closed
            assert_attachment_list(response.parse())

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    def test_delete_sends_delete_and_parses_result(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.delete(ATTACHMENT_PATH).mock(return_value=httpx.Response(200, json={"is_deleted": True}))

        result = client.documents.attachments.delete("att_01", document_id="doc_123")

        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "DELETE"
        assert request.url.query == b""
        assert request.content == b""
        assert isinstance(result, AttachmentDeleteResponse)
        assert result.is_deleted is True

    def test_delete_rejects_empty_path_params(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.attachments.delete("att_01", document_id="")

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `attachment_id` but received ''"):
            client.documents.attachments.delete("", document_id="doc_123")

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.delete(ATTACHMENT_PATH).mock(return_value=httpx.Response(200, json={"is_deleted": False}))

        response = client.documents.attachments.with_raw_response.delete("att_01", document_id="doc_123")

        assert response.is_closed is True
        result = response.parse()
        assert isinstance(result, AttachmentDeleteResponse)
        assert result.is_deleted is False

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.delete(ATTACHMENT_PATH).mock(return_value=httpx.Response(200, json={"is_deleted": True}))

        with client.documents.attachments.with_streaming_response.delete("att_01", document_id="doc_123") as response:
            assert not response.is_closed
            assert response.parse().is_deleted is True

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    def test_add_uploads_file_as_multipart(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post(ATTACHMENTS_PATH).mock(return_value=httpx.Response(200, json=FULL_ATTACHMENT))

        with pytest.warns(DeprecationWarning, match="deprecated"):
            attachment = client.documents.attachments.add(  # ty: ignore[deprecated]
                "doc_123", file=("delivery-note.pdf", PDF_BYTES, "application/pdf")
            )

        assert route.call_count == 1
        assert_multipart_upload(route.calls.last.request)
        assert_full_attachment(attachment)

    def test_add_rejects_empty_document_id(self, client: EInvoice) -> None:
        with (
            pytest.warns(DeprecationWarning, match="deprecated"),
            pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"),
        ):
            client.documents.attachments.add("", file=("a.pdf", PDF_BYTES))  # ty: ignore[deprecated]

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_add(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post(ATTACHMENTS_PATH).mock(return_value=httpx.Response(200, json=FULL_ATTACHMENT))

        with pytest.warns(DeprecationWarning, match="deprecated"):
            response = client.documents.attachments.with_raw_response.add(
                "doc_123", file=("delivery-note.pdf", PDF_BYTES, "application/pdf")
            )

        assert response.is_closed is True
        assert_multipart_upload(route.calls.last.request)
        assert_full_attachment(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_add(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.post(ATTACHMENTS_PATH).mock(return_value=httpx.Response(200, json=FULL_ATTACHMENT))

        stream = client.documents.attachments.with_streaming_response.add(
            "doc_123", file=("delivery-note.pdf", PDF_BYTES, "application/pdf")
        )
        assert route.call_count == 0  # the request (and the warning) only happen on enter

        with ExitStack() as stack:
            with pytest.warns(DeprecationWarning, match="deprecated"):
                response = stack.enter_context(stream)
            assert not response.is_closed
            assert_full_attachment(response.parse())

        assert response.is_closed is True
        assert_multipart_upload(route.calls.last.request)


class TestAsyncAttachments:
    def test_resource_exposes_wrapper_properties(self, async_client: AsyncEInvoice) -> None:
        raw = async_client.documents.attachments.with_raw_response
        streaming = async_client.documents.attachments.with_streaming_response

        assert isinstance(raw, AsyncAttachmentsResourceWithRawResponse)
        assert isinstance(streaming, AsyncAttachmentsResourceWithStreamingResponse)
        assert async_client.documents.attachments.with_raw_response is raw
        assert async_client.documents.attachments.with_streaming_response is streaming

    @pytest.mark.respx(base_url=base_url)
    async def test_retrieve_parses_attachment(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.get(ATTACHMENT_PATH).mock(return_value=httpx.Response(200, json=FULL_ATTACHMENT))

        attachment = await async_client.documents.attachments.retrieve("att_01", document_id="doc_123")

        assert route.call_count == 1
        assert route.calls.last.request.method == "GET"
        assert route.calls.last.request.url.query == b""
        assert_full_attachment(attachment)

    async def test_path_params_reject_empty_values(self, async_client: AsyncEInvoice) -> None:
        attachments = async_client.documents.attachments

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await attachments.retrieve("att_01", document_id="")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `attachment_id` but received ''"):
            await attachments.retrieve("", document_id="doc_123")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await attachments.list("")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await attachments.delete("att_01", document_id="")
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `attachment_id` but received ''"):
            await attachments.delete("", document_id="doc_123")
        with (
            pytest.warns(DeprecationWarning, match="deprecated"),
            pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"),
        ):
            await attachments.add("", file=("a.pdf", PDF_BYTES))  # ty: ignore[deprecated]

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get(ATTACHMENT_PATH).mock(
            return_value=httpx.Response(200, json=FULL_ATTACHMENT, headers={"x-request-id": "req_2"})
        )

        response = await async_client.documents.attachments.with_raw_response.retrieve("att_01", document_id="doc_123")

        assert isinstance(response, AsyncAPIResponse)
        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_2"
        assert_full_attachment(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get(ATTACHMENT_PATH).mock(return_value=httpx.Response(200, json=FULL_ATTACHMENT))

        async with async_client.documents.attachments.with_streaming_response.retrieve(
            "att_01", document_id="doc_123"
        ) as response:
            assert not response.is_closed
            assert_full_attachment(await response.parse())

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    async def test_list_returns_plain_list_of_attachments(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.get(ATTACHMENTS_PATH).mock(
            return_value=httpx.Response(200, json=[FULL_ATTACHMENT, MINIMAL_ATTACHMENT])
        )

        attachments = await async_client.documents.attachments.list("doc_123")

        assert route.call_count == 1
        assert route.calls.last.request.method == "GET"
        assert_attachment_list(attachments)

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get(ATTACHMENTS_PATH).mock(
            return_value=httpx.Response(200, json=[FULL_ATTACHMENT, MINIMAL_ATTACHMENT])
        )

        response = await async_client.documents.attachments.with_raw_response.list("doc_123")

        assert response.is_closed is True
        assert_attachment_list(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get(ATTACHMENTS_PATH).mock(
            return_value=httpx.Response(200, json=[FULL_ATTACHMENT, MINIMAL_ATTACHMENT])
        )

        async with async_client.documents.attachments.with_streaming_response.list("doc_123") as response:
            assert not response.is_closed
            assert_attachment_list(await response.parse())

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    async def test_delete_sends_delete_and_parses_result(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.delete(ATTACHMENT_PATH).mock(return_value=httpx.Response(200, json={"is_deleted": True}))

        result = await async_client.documents.attachments.delete("att_01", document_id="doc_123")

        assert route.call_count == 1
        assert route.calls.last.request.method == "DELETE"
        assert route.calls.last.request.content == b""
        assert isinstance(result, AttachmentDeleteResponse)
        assert result.is_deleted is True

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.delete(ATTACHMENT_PATH).mock(return_value=httpx.Response(200, json={"is_deleted": False}))

        response = await async_client.documents.attachments.with_raw_response.delete("att_01", document_id="doc_123")

        assert response.is_closed is True
        assert (await response.parse()).is_deleted is False

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.delete(ATTACHMENT_PATH).mock(return_value=httpx.Response(200, json={"is_deleted": True}))

        async with async_client.documents.attachments.with_streaming_response.delete(
            "att_01", document_id="doc_123"
        ) as response:
            assert not response.is_closed
            assert (await response.parse()).is_deleted is True

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    async def test_add_uploads_file_as_multipart(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post(ATTACHMENTS_PATH).mock(return_value=httpx.Response(200, json=FULL_ATTACHMENT))

        with pytest.warns(DeprecationWarning, match="deprecated"):
            attachment = await async_client.documents.attachments.add(  # ty: ignore[deprecated]
                "doc_123", file=("delivery-note.pdf", PDF_BYTES, "application/pdf")
            )

        assert route.call_count == 1
        assert_multipart_upload(route.calls.last.request)
        assert_full_attachment(attachment)

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_add(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post(ATTACHMENTS_PATH).mock(return_value=httpx.Response(200, json=FULL_ATTACHMENT))

        with pytest.warns(DeprecationWarning, match="deprecated"):
            response = await async_client.documents.attachments.with_raw_response.add(
                "doc_123", file=("delivery-note.pdf", PDF_BYTES, "application/pdf")
            )

        assert response.is_closed is True
        assert_multipart_upload(route.calls.last.request)
        assert_full_attachment(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_add(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.post(ATTACHMENTS_PATH).mock(return_value=httpx.Response(200, json=FULL_ATTACHMENT))

        # unlike the sync wrapper, the async one calls `add` (and so warns) straight away; the request
        # itself is only sent on enter
        with pytest.warns(DeprecationWarning, match="deprecated"):
            stream = async_client.documents.attachments.with_streaming_response.add(
                "doc_123", file=("delivery-note.pdf", PDF_BYTES, "application/pdf")
            )
        assert route.call_count == 0

        async with stream as response:
            assert not response.is_closed
            assert_full_attachment(await response.parse())

        assert response.is_closed is True
        assert_multipart_upload(route.calls.last.request)
