from typing import Literal

from didiator import CommandHandler

from domain.mapping import IClassMapper
from domain.models.requests import DeleteDisciplineRequest
from infrastructure.repositories import DisciplineRepository


class DeleteDisciplineHandler(CommandHandler[DeleteDisciplineRequest, Literal[True]]):
    def __init__(
            self, repo: DisciplineRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: DeleteDisciplineRequest) -> Literal[True]:
        response = await self.repo.direct_delete(command.id)
        return response
