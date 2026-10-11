from typing import List, Optional
from datetime import date
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["StatsRetrieveResponse", "Action"]


class Action(BaseModel):
    """Statistics for a specific action in a specific time period."""

    action: Literal["DOCUMENT_SENT", "DOCUMENT_RECEIVED"]
    """Type of action"""

    count: int
    """Number of occurrences of this action in this period"""

    stat_date: date
    """The date/period this stat represents.

    For DAY aggregation this is the specific day, for WEEK it's the start of the
    week, for MONTH it's the first day of the month
    """


class StatsRetrieveResponse(BaseModel):
    """Statistics response for a tenant."""

    actions: List[Action]
    """List of action statistics, one entry per aggregation period per action"""

    aggregation: Literal["DAY", "WEEK", "MONTH"]
    """Aggregation type used"""

    average_daily_usage: float
    """Average daily usage (total actions / total days)"""

    period_end: date
    """End date of the period"""

    period_start: date
    """Start date of the period"""

    tenant_id: str
    """Tenant ID"""

    total_days: int
    """Number of days in the period"""

    budget_estimation_days: Optional[float] = None
    """
    Estimated days until credits run out (credit_balance / average_daily_usage). 0.0
    if average_daily_usage is 0 or credit_balance is None
    """
