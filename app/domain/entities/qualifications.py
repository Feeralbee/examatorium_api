from .base import BaseEntity
from .competencies import CompetenceDomainEntity


class QualificationDomainEntity(BaseEntity):

    index: str
    name: str
    competencies: list[CompetenceDomainEntity]
