from typing import Literal

from didiator import CommandHandler
from loguru import logger

from domain.mapping import IClassMapper
from domain.models.requests import DeleteThemeRequest
from infrastructure.repositories import ThemeRepository


class DeleteThemeHandler(CommandHandler[DeleteThemeRequest, Literal[True]]):
    def __init__(
            self, repo: ThemeRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: DeleteThemeRequest) -> Literal[True]:
        response = await self.repo.direct_delete(command.id)
        return response
