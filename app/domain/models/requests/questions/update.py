from didiator import Command
from pydantic import BaseModel

from domain.entities import QuestionDomainEntity


class UpdateQuestionRequest(BaseModel, Command[QuestionDomainEntity]):

    id: str
    name: str
    is_task_question: bool = False
    theme_id: str
