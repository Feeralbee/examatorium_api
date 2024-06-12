import uuid
from typing import Optional

from loguru import logger
from pydantic import BaseModel, field_validator, model_validator


class BaseEntity(BaseModel):
    id: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        from_attributes = True

    @field_validator('id', mode='before')
    @classmethod
    def id_caster(cls, v):
        return str(v)
