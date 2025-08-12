# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import (
    LookupRetrieveResponse,
    LookupRetrieveParticipantsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestLookup:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: EInvoice) -> None:
        lookup = client.lookup.retrieve(
            peppol_id="peppol_id",
        )
        assert_matches_type(LookupRetrieveResponse, lookup, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: EInvoice) -> None:
        response = client.lookup.with_raw_response.retrieve(
            peppol_id="peppol_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lookup = response.parse()
        assert_matches_type(LookupRetrieveResponse, lookup, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: EInvoice) -> None:
        with client.lookup.with_streaming_response.retrieve(
            peppol_id="peppol_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lookup = response.parse()
            assert_matches_type(LookupRetrieveResponse, lookup, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_participants(self, client: EInvoice) -> None:
        lookup = client.lookup.retrieve_participants(
            query="query",
        )
        assert_matches_type(LookupRetrieveParticipantsResponse, lookup, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_participants_with_all_params(self, client: EInvoice) -> None:
        lookup = client.lookup.retrieve_participants(
            query="query",
            country_code="country_code",
        )
        assert_matches_type(LookupRetrieveParticipantsResponse, lookup, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve_participants(self, client: EInvoice) -> None:
        response = client.lookup.with_raw_response.retrieve_participants(
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lookup = response.parse()
        assert_matches_type(LookupRetrieveParticipantsResponse, lookup, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve_participants(self, client: EInvoice) -> None:
        with client.lookup.with_streaming_response.retrieve_participants(
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lookup = response.parse()
            assert_matches_type(LookupRetrieveParticipantsResponse, lookup, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncLookup:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEInvoice) -> None:
        lookup = await async_client.lookup.retrieve(
            peppol_id="peppol_id",
        )
        assert_matches_type(LookupRetrieveResponse, lookup, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.lookup.with_raw_response.retrieve(
            peppol_id="peppol_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lookup = await response.parse()
        assert_matches_type(LookupRetrieveResponse, lookup, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEInvoice) -> None:
        async with async_client.lookup.with_streaming_response.retrieve(
            peppol_id="peppol_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lookup = await response.parse()
            assert_matches_type(LookupRetrieveResponse, lookup, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_participants(self, async_client: AsyncEInvoice) -> None:
        lookup = await async_client.lookup.retrieve_participants(
            query="query",
        )
        assert_matches_type(LookupRetrieveParticipantsResponse, lookup, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_participants_with_all_params(self, async_client: AsyncEInvoice) -> None:
        lookup = await async_client.lookup.retrieve_participants(
            query="query",
            country_code="country_code",
        )
        assert_matches_type(LookupRetrieveParticipantsResponse, lookup, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve_participants(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.lookup.with_raw_response.retrieve_participants(
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lookup = await response.parse()
        assert_matches_type(LookupRetrieveParticipantsResponse, lookup, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve_participants(self, async_client: AsyncEInvoice) -> None:
        async with async_client.lookup.with_streaming_response.retrieve_participants(
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lookup = await response.parse()
            assert_matches_type(LookupRetrieveParticipantsResponse, lookup, path=["response"])

        assert cast(Any, response.is_closed) is True
