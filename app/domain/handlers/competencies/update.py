from didiator import CommandHandler
from domain.entities import CompetenceDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import UpdateCompetenceRequest
from infrastructure.repositories import CompetenceRepository


class UpdateCompetenceHandler(CommandHandler[UpdateCompetenceRequest, CompetenceDomainEntity]):
    def __init__(
            self, repo: CompetenceRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: UpdateCompetenceRequest) -> CompetenceDomainEntity:
        response = await self.repo.update(
            command.id,
            **command.model_dump(exclude={"id", }, exclude_unset=True)
        )
        return self.mapper.map(CompetenceDomainEntity, response)
