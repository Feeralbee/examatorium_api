from typing import Literal

from didiator import CommandHandler

from domain.mapping import IClassMapper
from domain.models.requests import DeleteGroupStudentRequest, DeleteGroupStudentByStudentIdRequest
from infrastructure.repositories import GroupStudentRepository


class DeleteGroupStudentHandler(CommandHandler[DeleteGroupStudentRequest, Literal[True]]):
    def __init__(
            self, repo: GroupStudentRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: DeleteGroupStudentRequest) -> Literal[True]:
        response = await self.repo.delete(command.id)
        return response


class DeleteGroupStudentByStudentIdHandler(CommandHandler[DeleteGroupStudentByStudentIdRequest, Literal[True]]):
    def __init__(
            self, repo: GroupStudentRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: DeleteGroupStudentByStudentIdRequest) -> Literal[True]:
        group_student = await self.repo.get_by(student_id=command.student_id)
        if group_student:
            await self.repo.delete(group_student.id)
        return True
