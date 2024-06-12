from didiator import CommandHandler

from domain.entities import GraduateThesisDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import CreateGraduateThesisRequest
from infrastructure.entities import GraduateThesisModel
from infrastructure.repositories import GraduateThesisRepository


class CreateGraduateThesisHandler(CommandHandler[CreateGraduateThesisRequest, GraduateThesisDomainEntity]):
    def __init__(
            self, repo: GraduateThesisRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: CreateGraduateThesisRequest) -> GraduateThesisDomainEntity:
        entity = self.mapper.map(GraduateThesisModel, command)
        response = await self.repo.create(entity)
        return self.mapper.map(GraduateThesisDomainEntity, response)
