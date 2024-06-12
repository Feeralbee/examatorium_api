from .base import BaseEntity


class QuestionDomainEntity(BaseEntity):

    name: str
    is_task_question: bool = False
    theme_id: str
