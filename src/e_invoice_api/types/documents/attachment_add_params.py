# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..._types import FileTypes

__all__ = ["AttachmentAddParams"]


class AttachmentAddParams(TypedDict, total=False):
    file: Required[FileTypes]
