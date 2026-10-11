from typing_extensions import Literal, TypeAlias

__all__ = ["DocumentState"]

DocumentState: TypeAlias = Literal["DRAFT", "TRANSIT", "FAILED", "SENT", "RECEIVED"]
