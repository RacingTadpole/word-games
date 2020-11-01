from typing import Dict, Iterable, Optional
from dataclasses import dataclass

@dataclass(frozen=True)
class Rung:
    previous: Optional['Rung']
    words: Iterable[str]
    path: Dict[str, Iterable[str]]

