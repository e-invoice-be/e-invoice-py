from typing_extensions import Literal, TypeAlias

__all__ = ["CurrencyCode"]

CurrencyCode: TypeAlias = Literal[
    "EUR", "USD", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD", "CNY", "INR", "SEK", "NOK", "DKK", "SGD", "HKD"
]
