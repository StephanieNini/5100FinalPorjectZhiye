from dataclasses import dataclass
from typing import List, Tuple

Position = Tuple[int, int]


@dataclass
class SearchResult:
    algorithm: str
    path: List[Position]
    explored_nodes: int
    runtime_ms: float

    @property
    def solved(self) -> bool:
        return len(self.path) > 0

    @property
    def path_length(self) -> int:
        if not self.path:
            return -1
        return max(0, len(self.path) - 1)
