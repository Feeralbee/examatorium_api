from didiator import CommandHandler

from domain.entities import ExamDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import GetExamRequest, GetExamListRequest, GetExamListByTeacherRequest, \
    GetExamListByGroupRequest
from domain.models.requests.exams.get import GetExamListByRequest
from infrastructure.repositories import ExamRepository


class GetExamHandler(CommandHandler[GetExamRequest, ExamDomainEntity]):
    def __init__(
            self, repo: ExamRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetExamRequest) -> ExamDomainEntity | None:
        response = await self.repo.get(command.id)
        if response:
            return self.mapper.map(ExamDomainEntity, response)


class GetExamListByTeacherHandler(CommandHandler[GetExamListByTeacherRequest, list[ExamDomainEntity]]):
    def __init__(
            self, repo: ExamRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetExamListByTeacherRequest) -> list[ExamDomainEntity]:
        response = await self.repo.get_by(teacher_id=command.teacher_id, is_many=True, with_unique=True)
        response = [self.mapper.map(ExamDomainEntity, i) for i in response]
        return response


class GetExamListByGroupHandler(CommandHandler[GetExamListByGroupRequest, list[ExamDomainEntity]]):
    def __init__(
            self, repo: ExamRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetExamListByGroupRequest) -> list[ExamDomainEntity]:
        response = await self.repo.get_by(group_id=command.group_id, is_many=True, with_unique=True)
        response = [self.mapper.map(ExamDomainEntity, i) for i in response]
        return response


class GetExamListByHandler(CommandHandler[GetExamListByRequest, list[ExamDomainEntity]]):
    def __init__(
            self, repo: ExamRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetExamListByRequest) -> list[ExamDomainEntity]:
        exams = await self.repo.get_by(**command.model_dump(), with_unique=True, is_many=True)
        exams = [self.mapper.map(ExamDomainEntity, i) for i in exams]
        return exams


class GetExamListHandler(CommandHandler[GetExamListRequest, list[ExamDomainEntity]]):
    def __init__(
            self, repo: ExamRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetExamListRequest) -> list[ExamDomainEntity]:
        exams = await self.repo.all(with_unique=True)
        exams = [self.mapper.map(ExamDomainEntity, i) for i in exams]
        return exams
