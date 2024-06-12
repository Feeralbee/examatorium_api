from didiator import CommandHandler
from domain.entities import GraduateThesisDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import UpdateGraduateThesisRequest
from infrastructure.repositories import GraduateThesisRepository


class UpdateGraduateThesisHandler(CommandHandler[UpdateGraduateThesisRequest, GraduateThesisDomainEntity]):
    def __init__(
            self, repo: GraduateThesisRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: UpdateGraduateThesisRequest) -> GraduateThesisDomainEntity:
        response = await self.repo.update(
            command.id,
            **command.model_dump(exclude={"id", }, exclude_unset=True)
        )
        return self.mapper.map(GraduateThesisDomainEntity, response)
