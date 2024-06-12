from typing import Literal

from didiator import CommandHandler

from domain.mapping import IClassMapper
from domain.models.requests import DeleteGraduateThesisRequest
from infrastructure.repositories import GraduateThesisRepository


class DeleteGraduateThesisHandler(CommandHandler[DeleteGraduateThesisRequest, Literal[True]]):
    def __init__(
            self, repo: GraduateThesisRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: DeleteGraduateThesisRequest) -> Literal[True]:
        response = await self.repo.direct_delete(command.id)
        return response
