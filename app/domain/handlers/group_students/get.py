from didiator import CommandHandler

from domain.entities import GroupStudentDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import GetGroupStudentRequest, GetGroupStudentListRequest, GetStudentGroupRequest
from infrastructure.repositories import GroupStudentRepository


class GetGroupStudentHandler(CommandHandler[GetGroupStudentRequest, GroupStudentDomainEntity]):
    def __init__(
            self, repo: GroupStudentRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetGroupStudentRequest) -> GroupStudentDomainEntity | None:
        group_student = await self.repo.get(command.id)
        if group_student:
            group_student = self.mapper.map(GroupStudentDomainEntity, group_student)
            return group_student


class GetStudentGroupHandler(CommandHandler[GetStudentGroupRequest, GroupStudentDomainEntity]):
    def __init__(
            self, repo: GroupStudentRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetStudentGroupRequest) -> GroupStudentDomainEntity | None:
        group_student = await self.repo.get_by(student_id=command.student_id)
        if group_student:
            group_student = self.mapper.map(GroupStudentDomainEntity, group_student)
            return group_student


class GetGroupStudentListHandler(CommandHandler[GetGroupStudentListRequest, list[GroupStudentDomainEntity]]):
    def __init__(
            self, repo: GroupStudentRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetGroupStudentListRequest) -> list[GroupStudentDomainEntity]:
        group_students = await self.repo.all(with_unique=True)
        groups_students = [self.mapper.map(GroupStudentDomainEntity, i) for i in group_students]
        return groups_students
