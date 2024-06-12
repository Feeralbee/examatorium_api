from typing import Literal

from didiator import CommandHandler

from domain.mapping import IClassMapper
from domain.models.requests import DeleteExamRequest
from infrastructure.repositories import ExamRepository


class DeleteExamHandler(CommandHandler[DeleteExamRequest, Literal[True]]):
    def __init__(
            self, repo: ExamRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: DeleteExamRequest) -> Literal[True]:
        response = await self.repo.direct_delete(command.id)
        return response
