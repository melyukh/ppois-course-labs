from typing import Protocol, Any

class IntegerMapped(Protocol):
    def __index__(self, other: Any) -> int: 
        ...