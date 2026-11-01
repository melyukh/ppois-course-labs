from typing import Protocol, Any

class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool: 
        ...