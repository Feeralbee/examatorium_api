from abc import ABC, abstractmethod
from typing import TypeVar, Any, Type

T = TypeVar("T", bound=Any)
V = TypeVar("V", bound=Any)


class IClassMapper(ABC):

    @abstractmethod
    def map(self, to_cls: Type[V], obj: T) -> V:
        raise NotImplementedError


