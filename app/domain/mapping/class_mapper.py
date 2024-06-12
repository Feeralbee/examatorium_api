import types
import typing
from typing import Type

from loguru import logger

from domain.mapping.abstraction import IClassMapper, IBaseMappingConfiguration
from domain.mapping.abstraction.class_mapper import V, T


class ClassMapper(IClassMapper):
    def __init__(self, config: IBaseMappingConfiguration):
        self._config = config

    def map(self, to_cls: Type[V], obj: T) -> V:
        to_cls_type = type(to_cls)
        obj_type = type(obj)

        if type(to_cls) == types.GenericAlias:
            to_cls_type = typing.get_origin(to_cls)

        if obj_type == list and to_cls_type == list:
            is_uct = all(isinstance(item, type(obj[0])) for item in obj)
            if is_uct:
                uct = type(obj[0])
                mapper_obj = self._config.get_mapper(list[uct], to_cls)

        else:
            mapper_obj = self._config.get_mapper(type(obj), to_cls)

        mapper = mapper_obj.mapper
        return mapper.map(obj)
