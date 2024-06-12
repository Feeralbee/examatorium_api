import typing
from dataclasses import dataclass
from typing import Type

from loguru import logger

from domain.mapping.abstraction import IBaseMappingConfiguration, IBaseMapper
from domain.mapping.abstraction.mapping_configuration import T, V, IMapperConfigurationItem


@dataclass
class MapperConfigurationItem:
    from_cls: Type[T]
    to_cls: Type[V]
    mapper: IBaseMapper[T, V]


class MappingConfiguration(IBaseMappingConfiguration):
    def __init__(self):
        self.mappers: list[IMapperConfigurationItem] = []

    def get_mapper(self, from_cls: Type[T], to_cls: Type[V]) -> IMapperConfigurationItem:
        for mapper in self.mappers:
            if mapper.from_cls == from_cls and mapper.to_cls == to_cls:
                return mapper

    def add_mapper(self, from_cls: Type[T], to_cls: Type[V], mapper: IBaseMapper[T, V]) -> IMapperConfigurationItem:
        mapper_obj = MapperConfigurationItem(from_cls=from_cls, to_cls=to_cls, mapper=mapper)
        self.mappers.append(mapper_obj)
        return mapper_obj
