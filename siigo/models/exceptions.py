from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SiigoError:
    code: str
    message: str
    params: Optional[List[str]] = None
    deatil: Optional[str] = None

    def to_str(self) -> str:
        return f'{self.code}: {self.message}'
