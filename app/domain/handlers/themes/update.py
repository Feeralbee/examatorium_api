from didiator import CommandHandler
from domain.entities import ThemeDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import UpdateThemeRequest
from infrastructure.repositories import ThemeRepository


class UpdateThemeHandler(CommandHandler[UpdateThemeRequest, ThemeDomainEntity]):
    def __init__(
            self, repo: ThemeRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: UpdateThemeRequest) -> ThemeDomainEntity:
        response = await self.repo.update(
            command.id,
            **command.model_dump(exclude={"id", }, exclude_unset=True)
        )
        return self.mapper.map(ThemeDomainEntity, response)
