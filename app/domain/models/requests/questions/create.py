from didiator import Command
from pydantic import BaseModel

from domain.entities import QuestionDomainEntity


class CreateQuestionRequest(BaseModel, Command[QuestionDomainEntity]):
    name: str
    is_task_question: bool = False
    theme_id: str
