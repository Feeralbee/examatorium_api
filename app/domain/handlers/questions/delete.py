from typing import Literal

from didiator import CommandHandler

from domain.mapping import IClassMapper
from domain.models.requests import DeleteQuestionRequest
from infrastructure.repositories import QuestionRepository


class DeleteQuestionHandler(CommandHandler[DeleteQuestionRequest, Literal[True]]):
    def __init__(
            self, repo: QuestionRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: DeleteQuestionRequest) -> Literal[True]:
        response = await self.repo.delete(command.id)
        return response
