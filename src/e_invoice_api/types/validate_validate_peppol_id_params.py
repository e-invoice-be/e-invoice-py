# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ValidateValidatePeppolIDParams"]


class ValidateValidatePeppolIDParams(TypedDict, total=False):
    peppol_id: Required[str]
    """Peppol ID in the format `<scheme>:<id>`.

    Example: `0208:1018265814` for a Belgian company.
    """
