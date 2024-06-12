from .base import BaseEntity


class GroupStudentDomainEntity(BaseEntity):

    student_id: str
    group_id: str
