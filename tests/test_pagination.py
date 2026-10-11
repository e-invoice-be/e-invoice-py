from __future__ import annotations

import os
from typing import Any, List, cast

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, AsyncEInvoice

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

DOCUMENT_IDS = ["doc_1", "doc_2", "doc_3"]
PAGE_SIZE = 2


def three_documents_over_two_pages(request: httpx.Request) -> httpx.Response:
    page = int(request.url.params.get("page", "1"))
    ids = DOCUMENT_IDS[(page - 1) * PAGE_SIZE : page * PAGE_SIZE]
    return httpx.Response(
        200,
        json={
            "items": [{"id": id_, "created_at": "2026-04-01T08:30:00Z"} for id_ in ids],
            "total": 3,
            "page": page,
            "page_size": PAGE_SIZE,
            "pages": 2,
            "has_next_page": page < 2,
        },
    )


def requested_pages(respx_mock: MockRouter) -> List[str]:
    requests: List[httpx.Request] = [call.request for call in cast(Any, respx_mock.calls)]
    return [request.url.params.get("page", "1") for request in requests]


@pytest.mark.respx(base_url=base_url)
def test_auto_pagination_stops_at_last_page(respx_mock: MockRouter, client: EInvoice) -> None:
    respx_mock.get("/api/inbox/").mock(side_effect=three_documents_over_two_pages)

    ids = [document.id for document in client.inbox.list()]

    assert ids == ["doc_1", "doc_2", "doc_3"]
    assert requested_pages(respx_mock) == ["1", "2"]


@pytest.mark.respx(base_url=base_url)
async def test_async_auto_pagination_stops_at_last_page(respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
    respx_mock.get("/api/inbox/").mock(side_effect=three_documents_over_two_pages)

    ids = [document.id async for document in async_client.inbox.list()]

    assert ids == ["doc_1", "doc_2", "doc_3"]
    assert requested_pages(respx_mock) == ["1", "2"]
