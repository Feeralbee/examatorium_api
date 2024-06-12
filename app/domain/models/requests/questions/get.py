from didiator import Command
from pydantic import BaseModel

from domain.entities import QuestionDomainEntity


class GetQuestionRequest(BaseModel, Command[QuestionDomainEntity]):
    id: str


class GetQuestionListRequest(BaseModel, Command[list[QuestionDomainEntity]]):
    pass
