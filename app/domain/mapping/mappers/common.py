import dataclasses
from typing import TypeVar, Any, Generic

from pydantic import BaseModel, TypeAdapter

from domain.mapping.abstraction import IBaseMapper

TPydantic = TypeVar("TPydantic", bound=BaseModel)
TOutPydantic = TypeVar("TOutPydantic", bound=BaseModel)
TDataclass = TypeVar("TDataclass", bound=Any)
TDict = TypeVar("TDict", bound=dict)
TListPydantic = TypeVar("TListPydantic", bound=list[BaseModel])
TListModel = TypeVar("TListModel", bound=list[Any])
TModel = TypeVar("TModel", bound=Any)


class DTPMapper(Generic[TDataclass, TPydantic], IBaseMapper[TDataclass, TPydantic]):
    """Dataclass to Pydantic model"""

    def map(self, obj: TDataclass) -> TPydantic:
        to_model = self.__orig_class__.__args__[1]
        return to_model(**dataclasses.asdict(obj))


class PTDMapper(Generic[TPydantic, TDataclass], IBaseMapper[TPydantic, TDataclass]):
    """Pydantic to Dataclass model"""

    def map(self, obj: TPydantic) -> TDataclass:
        to_class = self.__orig_class__.__args__[1]
        return to_class(**obj.dict())


class PTPMapper(Generic[TPydantic, TOutPydantic], IBaseMapper[TPydantic, TOutPydantic]):
    """Pydantic to Pydantic model"""

    def map(self, obj: TPydantic) -> TOutPydantic:
        to_model = self.__orig_class__.__args__[1]
        return to_model(**obj.dict())


class DictTPMapper(Generic[TDict, TOutPydantic], IBaseMapper[TDict, TOutPydantic]):
    """Dict to Pydantic model"""

    def map(self, obj: TDict) -> TOutPydantic:
        to_model = self.__orig_class__.__args__[1]
        return to_model(**obj)


class DictTPMapper(Generic[TDict, TOutPydantic], IBaseMapper[TDict, TOutPydantic]):
    """Dict to Pydantic model"""

    def map(self, obj: TDict) -> TOutPydantic:
        to_model = self.__orig_class__.__args__[1]
        return to_model(**obj)


class LMTLPMapper(Generic[TListModel, TListPydantic], IBaseMapper[TListModel, TListPydantic]):
    """List Models to List Pydantic models"""

    def map(self, obj: TListModel) -> TListPydantic:
        return TypeAdapter(self.__orig_class__.__args__[1]).validate_python(obj)


class MTPMapper(Generic[TModel, TPydantic], IBaseMapper[TModel, TPydantic]):
    """Model to Pydantic model"""

    def map(self, obj: TListModel) -> TListPydantic:
        to_model: BaseModel = self.__orig_class__.__args__[1]
        return to_model.from_orm(obj)


class PTMMapper(Generic[TPydantic, TModel], IBaseMapper[TPydantic, TModel]):
    """Pydantic to Model"""

    def map(self, obj: TPydantic) -> TListPydantic:
        to_model: TModel = self.__orig_class__.__args__[1]
        return to_model(**obj.dict())
