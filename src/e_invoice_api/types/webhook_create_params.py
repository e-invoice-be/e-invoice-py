# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["WebhookCreateParams"]


class WebhookCreateParams(TypedDict, total=False):
    events: Required[List[str]]

    url: Required[str]

    enabled: bool
