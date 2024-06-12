from didiator import CommandHandler

from domain.entities import ExamDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import CreateExamRequest
from infrastructure.entities import ExamModel
from infrastructure.repositories import ExamRepository


class CreateExamHandler(CommandHandler[CreateExamRequest, ExamDomainEntity]):
    def __init__(
            self, repo: ExamRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: CreateExamRequest) -> ExamDomainEntity:
        entity = self.mapper.map(ExamModel, command)
        response = await self.repo.create(entity)
        return self.mapper.map(ExamDomainEntity, response)
