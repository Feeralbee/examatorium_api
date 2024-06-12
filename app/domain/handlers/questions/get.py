from didiator import CommandHandler

from domain.entities import QuestionDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import GetQuestionRequest, GetQuestionListRequest
from infrastructure.repositories import QuestionRepository


class GetQuestionHandler(CommandHandler[GetQuestionRequest, QuestionDomainEntity]):
    def __init__(
            self, repo: QuestionRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetQuestionRequest) -> QuestionDomainEntity | None:
        response = await self.repo.get(command.id)
        if response:
            return self.mapper.map(QuestionDomainEntity, response)


class GetQuestionListHandler(CommandHandler[GetQuestionListRequest, list[QuestionDomainEntity]]):
    def __init__(
            self, repo: QuestionRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetQuestionListRequest) -> list[QuestionDomainEntity]:
        questions = await self.repo.all()
        questions = [self.mapper.map(QuestionDomainEntity, i) for i in questions]
        return questions
