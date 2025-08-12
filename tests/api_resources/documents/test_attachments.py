# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types.documents import (
    DocumentAttachment,
    AttachmentListResponse,
    AttachmentDeleteResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAttachments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: EInvoice) -> None:
        attachment = client.documents.attachments.retrieve(
            attachment_id="attachment_id",
            document_id="document_id",
        )
        assert_matches_type(DocumentAttachment, attachment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: EInvoice) -> None:
        response = client.documents.attachments.with_raw_response.retrieve(
            attachment_id="attachment_id",
            document_id="document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        attachment = response.parse()
        assert_matches_type(DocumentAttachment, attachment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: EInvoice) -> None:
        with client.documents.attachments.with_streaming_response.retrieve(
            attachment_id="attachment_id",
            document_id="document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            attachment = response.parse()
            assert_matches_type(DocumentAttachment, attachment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.attachments.with_raw_response.retrieve(
                attachment_id="attachment_id",
                document_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `attachment_id` but received ''"):
            client.documents.attachments.with_raw_response.retrieve(
                attachment_id="",
                document_id="document_id",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: EInvoice) -> None:
        attachment = client.documents.attachments.list(
            "document_id",
        )
        assert_matches_type(AttachmentListResponse, attachment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: EInvoice) -> None:
        response = client.documents.attachments.with_raw_response.list(
            "document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        attachment = response.parse()
        assert_matches_type(AttachmentListResponse, attachment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: EInvoice) -> None:
        with client.documents.attachments.with_streaming_response.list(
            "document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            attachment = response.parse()
            assert_matches_type(AttachmentListResponse, attachment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_list(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.attachments.with_raw_response.list(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete(self, client: EInvoice) -> None:
        attachment = client.documents.attachments.delete(
            attachment_id="attachment_id",
            document_id="document_id",
        )
        assert_matches_type(AttachmentDeleteResponse, attachment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: EInvoice) -> None:
        response = client.documents.attachments.with_raw_response.delete(
            attachment_id="attachment_id",
            document_id="document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        attachment = response.parse()
        assert_matches_type(AttachmentDeleteResponse, attachment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: EInvoice) -> None:
        with client.documents.attachments.with_streaming_response.delete(
            attachment_id="attachment_id",
            document_id="document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            attachment = response.parse()
            assert_matches_type(AttachmentDeleteResponse, attachment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.attachments.with_raw_response.delete(
                attachment_id="attachment_id",
                document_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `attachment_id` but received ''"):
            client.documents.attachments.with_raw_response.delete(
                attachment_id="",
                document_id="document_id",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_add(self, client: EInvoice) -> None:
        attachment = client.documents.attachments.add(
            document_id="document_id",
            file=b"raw file contents",
        )
        assert_matches_type(DocumentAttachment, attachment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_add(self, client: EInvoice) -> None:
        response = client.documents.attachments.with_raw_response.add(
            document_id="document_id",
            file=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        attachment = response.parse()
        assert_matches_type(DocumentAttachment, attachment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_add(self, client: EInvoice) -> None:
        with client.documents.attachments.with_streaming_response.add(
            document_id="document_id",
            file=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            attachment = response.parse()
            assert_matches_type(DocumentAttachment, attachment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_add(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.attachments.with_raw_response.add(
                document_id="",
                file=b"raw file contents",
            )


class TestAsyncAttachments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEInvoice) -> None:
        attachment = await async_client.documents.attachments.retrieve(
            attachment_id="attachment_id",
            document_id="document_id",
        )
        assert_matches_type(DocumentAttachment, attachment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.documents.attachments.with_raw_response.retrieve(
            attachment_id="attachment_id",
            document_id="document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        attachment = await response.parse()
        assert_matches_type(DocumentAttachment, attachment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEInvoice) -> None:
        async with async_client.documents.attachments.with_streaming_response.retrieve(
            attachment_id="attachment_id",
            document_id="document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            attachment = await response.parse()
            assert_matches_type(DocumentAttachment, attachment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.documents.attachments.with_raw_response.retrieve(
                attachment_id="attachment_id",
                document_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `attachment_id` but received ''"):
            await async_client.documents.attachments.with_raw_response.retrieve(
                attachment_id="",
                document_id="document_id",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncEInvoice) -> None:
        attachment = await async_client.documents.attachments.list(
            "document_id",
        )
        assert_matches_type(AttachmentListResponse, attachment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.documents.attachments.with_raw_response.list(
            "document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        attachment = await response.parse()
        assert_matches_type(AttachmentListResponse, attachment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEInvoice) -> None:
        async with async_client.documents.attachments.with_streaming_response.list(
            "document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            attachment = await response.parse()
            assert_matches_type(AttachmentListResponse, attachment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.documents.attachments.with_raw_response.list(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncEInvoice) -> None:
        attachment = await async_client.documents.attachments.delete(
            attachment_id="attachment_id",
            document_id="document_id",
        )
        assert_matches_type(AttachmentDeleteResponse, attachment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.documents.attachments.with_raw_response.delete(
            attachment_id="attachment_id",
            document_id="document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        attachment = await response.parse()
        assert_matches_type(AttachmentDeleteResponse, attachment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEInvoice) -> None:
        async with async_client.documents.attachments.with_streaming_response.delete(
            attachment_id="attachment_id",
            document_id="document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            attachment = await response.parse()
            assert_matches_type(AttachmentDeleteResponse, attachment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.documents.attachments.with_raw_response.delete(
                attachment_id="attachment_id",
                document_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `attachment_id` but received ''"):
            await async_client.documents.attachments.with_raw_response.delete(
                attachment_id="",
                document_id="document_id",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_add(self, async_client: AsyncEInvoice) -> None:
        attachment = await async_client.documents.attachments.add(
            document_id="document_id",
            file=b"raw file contents",
        )
        assert_matches_type(DocumentAttachment, attachment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_add(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.documents.attachments.with_raw_response.add(
            document_id="document_id",
            file=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        attachment = await response.parse()
        assert_matches_type(DocumentAttachment, attachment, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncEInvoice) -> None:
        async with async_client.documents.attachments.with_streaming_response.add(
            document_id="document_id",
            file=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            attachment = await response.parse()
            assert_matches_type(DocumentAttachment, attachment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_add(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.documents.attachments.with_raw_response.add(
                document_id="",
                file=b"raw file contents",
            )
