from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Any, Type, Protocol

from domain.mapping.abstraction import IBaseMapper

T = TypeVar("T", bound=Any)
V = TypeVar("V", bound=Any)


@dataclass
class IMapperConfigurationItem(Protocol):
    from_cls: Type[T]
    to_cls: Type[V]
    mapper: IBaseMapper[T, V]


class IBaseMappingConfiguration(ABC):

    @abstractmethod
    def get_mapper(self, from_cls: Type[T], to_cls: Type[V]) -> IMapperConfigurationItem:
        pass

    @abstractmethod
    def add_mapper(self, from_cls: Type[T], to_cls: Type[V], mapper: IBaseMapper[T, V]):
        pass
