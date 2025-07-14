# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["LookupRetrieveParticipantsParams"]


class LookupRetrieveParticipantsParams(TypedDict, total=False):
    query: Required[str]
    """Query to lookup"""

    country_code: Optional[str]
    """Country code of the company to lookup.

    If not provided, the search will be global.
    """
