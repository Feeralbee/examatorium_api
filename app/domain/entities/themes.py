from .questions import QuestionDomainEntity
from .base import BaseEntity
from .exams import ExamDomainEntity


class ThemeDomainEntity(BaseEntity):

    name: str
    exam_id: str
    exam: ExamDomainEntity
    questions: list[QuestionDomainEntity]
