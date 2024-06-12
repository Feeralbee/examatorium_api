from typing import Literal

from didiator import CommandHandler

from domain.mapping import IClassMapper
from domain.models.requests import DeleteCompetenceRequest
from infrastructure.repositories import CompetenceRepository


class DeleteCompetenceHandler(CommandHandler[DeleteCompetenceRequest, Literal[True]]):
    def __init__(
            self, repo: CompetenceRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: DeleteCompetenceRequest) -> Literal[True]:
        response = await self.repo.direct_delete(command.id)
        return response
