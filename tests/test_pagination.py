from __future__ import annotations

import os
from typing import Any, Dict, List

import pytest
from respx import MockRouter

from tests.utils import serve_pages, sent_queries
from e_invoice_api import EInvoice, AsyncEInvoice

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

DOCUMENTS: List[Dict[str, Any]] = [
    {"id": id_, "created_at": "2026-04-01T08:30:00Z"} for id_ in ("doc_1", "doc_2", "doc_3")
]


@pytest.mark.respx(base_url=base_url)
def test_auto_pagination_stops_at_last_page(respx_mock: MockRouter, client: EInvoice) -> None:
    respx_mock.get("/api/inbox/").mock(side_effect=serve_pages(DOCUMENTS, page_size=2))

    ids = [document.id for document in client.inbox.list()]

    assert ids == ["doc_1", "doc_2", "doc_3"]
    assert sent_queries(respx_mock) == [{}, {"page": "2"}]


@pytest.mark.respx(base_url=base_url)
async def test_async_auto_pagination_stops_at_last_page(respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
    respx_mock.get("/api/inbox/").mock(side_effect=serve_pages(DOCUMENTS, page_size=2))

    ids = [document.id async for document in async_client.inbox.list()]

    assert ids == ["doc_1", "doc_2", "doc_3"]
    assert sent_queries(respx_mock) == [{}, {"page": "2"}]
