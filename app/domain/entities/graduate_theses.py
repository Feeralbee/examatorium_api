from .base import BaseEntity
from .groups import GroupDomainEntity


class GraduateThesisDomainEntity(BaseEntity):

    group_id: str
    group: GroupDomainEntity
