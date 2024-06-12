from .base import BaseEntity
from .disciplines import DisciplineDomainEntity
from .users import UserDomainEntity
from .groups import GroupDomainEntity


class GraduateThesisDomainEntity(BaseEntity):

    group_id: str
    group: GroupDomainEntity
