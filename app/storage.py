from dataclasses import dataclass
from typing import Any, Dict, Hashable
import time


class ValueDoesNotExist:
    pass


@dataclass(frozen=True)
class ExpireValueContainer:
    value: Any
    expired_date: float  # expired date in milliseconds

    def is_expired(self) -> bool:
        return (time.time() * 1000) > self.expired_date


@dataclass
class Storage:
    storage: Dict[Hashable, Any]

    def set(self, key: Hashable, value: Any, expire: int | None = None) -> None:
        """Save value in storage by hashable key

        Args:
            key (Hashable): key
            value (Any): value to save
            expire (int | None, optional): expire time in milliseconds
        """
        if expire is None:
            self.storage[key] = value
            return
        time_in_ms = time.time_ns() // 1000000
        self.storage[key] = ExpireValueContainer(value, time_in_ms + expire)
        return

    def get(self, key: Hashable) -> Any | ValueDoesNotExist:
        try:
            value = self.storage[key]
            print(f'{value=}')
            if isinstance(value, ExpireValueContainer):
                if value.is_expired():
                    print(f'is expired')
                    del self.storage[key]
                    return ValueDoesNotExist
                return value.value
            return value
        except KeyError:
            return ValueDoesNotExist
