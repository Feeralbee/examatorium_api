from didiator import CommandHandler

from domain.entities import CompetenceDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import CreateCompetenceRequest
from infrastructure.entities import CompetenceModel
from infrastructure.repositories import CompetenceRepository


class CreateCompetenceHandler(CommandHandler[CreateCompetenceRequest, CompetenceDomainEntity]):
    def __init__(
            self, repo: CompetenceRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: CreateCompetenceRequest) -> CompetenceDomainEntity:
        entity = self.mapper.map(CompetenceModel, command)
        response = await self.repo.create(entity)
        return self.mapper.map(CompetenceDomainEntity, response)
