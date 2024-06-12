from didiator import CommandHandler

from domain.entities import QuestionDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import CreateQuestionRequest
from infrastructure.entities import QuestionModel
from infrastructure.repositories import QuestionRepository


class CreateQuestionHandler(CommandHandler[CreateQuestionRequest, QuestionDomainEntity]):
    def __init__(
            self, repo: QuestionRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: CreateQuestionRequest) -> QuestionDomainEntity:
        entity = self.mapper.map(QuestionModel, command)
        response = await self.repo.create(entity)
        return self.mapper.map(QuestionDomainEntity, response)
