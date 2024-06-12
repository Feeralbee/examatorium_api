from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any

T = TypeVar("T", bound=Any)
V = TypeVar("V", bound=Any)


class IBaseMapper(Generic[T, V], ABC):
    @abstractmethod
    def map(self, obj: T) -> V:
        pass
