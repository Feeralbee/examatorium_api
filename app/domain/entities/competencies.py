from misc.enums import CompetenceTypes
from .base import BaseEntity


class CompetenceDomainEntity(BaseEntity):

    name: str
    type: CompetenceTypes
    index: str
