from __future__ import annotations

import os
import contextlib
from typing import Any, Dict, List, Callable, Generator, cast

import httpx
from respx import Route, MockRouter

from e_invoice_api._types import Omit


@contextlib.contextmanager
def update_env(**new_env: str | Omit) -> Generator[None, None, None]:
    old = os.environ.copy()

    try:
        for name, value in new_env.items():
            if isinstance(value, Omit):
                os.environ.pop(name, None)
            else:
                os.environ[name] = value

        yield None
    finally:
        os.environ.clear()
        os.environ.update(old)


def page_payload(items: List[Dict[str, Any]], *, page: int = 1, pages: int = 1) -> Dict[str, Any]:
    return {
        "items": items,
        "total": len(items),
        "page": page,
        "page_size": max(len(items), 1),
        "pages": pages,
        "has_next_page": page < pages,
    }


def serve_pages(items: List[Dict[str, Any]], *, page_size: int = 1) -> Callable[[httpx.Request], httpx.Response]:
    pages = -(-len(items) // page_size)

    def respond(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        return httpx.Response(
            200,
            json={
                "items": items[(page - 1) * page_size : page * page_size],
                "total": len(items),
                "page": page,
                "page_size": page_size,
                "pages": pages,
                "has_next_page": page < pages,
            },
        )

    return respond


def sent_queries(route: Route | MockRouter) -> List[Dict[str, str]]:
    requests: List[httpx.Request] = [call.request for call in cast(Any, route.calls)]
    return [dict(request.url.params) for request in requests]
