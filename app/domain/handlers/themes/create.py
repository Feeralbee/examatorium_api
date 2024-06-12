from didiator import CommandHandler

from domain.entities import ThemeDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import CreateThemeRequest
from infrastructure.entities import ThemeModel
from infrastructure.repositories import ThemeRepository


class CreateThemeHandler(CommandHandler[CreateThemeRequest, ThemeDomainEntity]):
    def __init__(
            self, repo: ThemeRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: CreateThemeRequest) -> ThemeDomainEntity:
        entity = self.mapper.map(ThemeModel, command)
        response = await self.repo.create(entity)
        return self.mapper.map(ThemeDomainEntity, response)
