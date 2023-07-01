from dataclasses import dataclass
from typing import Any, Dict, Hashable


class ValueDoesNotExist:
    pass


@dataclass
class Storage:
    storage: Dict[Hashable, Any]

    def set(self, key: Hashable, value: Any) -> None:
        self.storage[key] = value

    def get(self, key: Hashable) -> Any | ValueDoesNotExist:
        try:
            return self.storage[key]
        except KeyError:
            return ValueDoesNotExist
