from typing import Literal

from didiator import CommandHandler

from domain.mapping import IClassMapper
from domain.models.requests import DeleteCourseWorkRequest
from infrastructure.repositories import CourseWorkRepository


class DeleteCourseWorkHandler(CommandHandler[DeleteCourseWorkRequest, Literal[True]]):
    def __init__(
            self, repo: CourseWorkRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: DeleteCourseWorkRequest) -> Literal[True]:
        response = await self.repo.direct_delete(command.id)
        return response
