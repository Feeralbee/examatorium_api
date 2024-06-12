from didiator import CommandHandler
from loguru import logger

from domain.entities import ThemeDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import GetThemeRequest, GetThemeListRequest, GetExamThemesRequest
from infrastructure.repositories import ThemeRepository


class GetThemeHandler(CommandHandler[GetThemeRequest, ThemeDomainEntity]):
    def __init__(
            self, repo: ThemeRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetThemeRequest) -> ThemeDomainEntity | None:
        response = await self.repo.get(command.id)
        if response:
            return self.mapper.map(ThemeDomainEntity, response)


class GetExamThemesHandler(CommandHandler[GetExamThemesRequest, list[ThemeDomainEntity]]):
    def __init__(
            self, repo: ThemeRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetExamThemesRequest) -> list[ThemeDomainEntity]:
        themes = await self.repo.get_by(exam_id=command.exam_id, with_unique=True, is_many=True)
        themes = [self.mapper.map(ThemeDomainEntity, i) for i in themes]
        return themes


class GetThemeListHandler(CommandHandler[GetThemeListRequest, list[ThemeDomainEntity]]):
    def __init__(
            self, repo: ThemeRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetThemeListRequest) -> list[ThemeDomainEntity]:
        themes = await self.repo.all(with_unique=True)
        themes = [self.mapper.map(ThemeDomainEntity, i) for i in themes]
        return themes
