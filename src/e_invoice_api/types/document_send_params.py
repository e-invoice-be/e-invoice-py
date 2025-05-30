# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["DocumentSendParams"]


class DocumentSendParams(TypedDict, total=False):
    email: Optional[str]

    receiver_peppol_id: Optional[str]

    receiver_peppol_scheme: Optional[str]

    sender_peppol_id: Optional[str]

    sender_peppol_scheme: Optional[str]
