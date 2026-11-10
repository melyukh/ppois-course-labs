from typing import Protocol, Any

class IntegerMapped(Protocol):
    def __int__(self, other: Any) -> int: 
        ...