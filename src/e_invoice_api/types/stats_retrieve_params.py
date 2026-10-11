from __future__ import annotations

from typing import Union, Optional
from datetime import date
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["StatsRetrieveParams"]


class StatsRetrieveParams(TypedDict, total=False):
    aggregation: Optional[Literal["DAY", "WEEK", "MONTH"]]
    """Aggregation type: DAY, WEEK, or MONTH. Defaults to DAY."""

    end_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """End date in yyyy-mm-dd format.

    If not provided, queries to latest available data.
    """

    start_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """Start date in yyyy-mm-dd format.

    If not provided, queries from earliest available data.
    """
