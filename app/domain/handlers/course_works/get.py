from didiator import CommandHandler

from domain.entities import CourseWorkDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import GetCourseWorkRequest, GetCourseWorkListRequest, GetCourseWorkListByGroupRequest
from infrastructure.repositories import CourseWorkRepository


class GetCourseWorkHandler(CommandHandler[GetCourseWorkRequest, CourseWorkDomainEntity]):
    def __init__(
            self, repo: CourseWorkRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetCourseWorkRequest) -> CourseWorkDomainEntity | None:
        response = await self.repo.get(command.id)
        if response:
            return self.mapper.map(CourseWorkDomainEntity, response)


class GetCourseWorkListByGroupHandler(CommandHandler[GetCourseWorkListByGroupRequest, list[CourseWorkDomainEntity]]):
    def __init__(
            self, repo: CourseWorkRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetCourseWorkListByGroupRequest) -> list[CourseWorkDomainEntity]:
        response = await self.repo.get_by(group_id=command.group_id, is_many=True, with_unique=True)
        response = [self.mapper.map(CourseWorkDomainEntity, i) for i in response]
        return response


class GetCourseWorkListHandler(CommandHandler[GetCourseWorkListRequest, list[CourseWorkDomainEntity]]):
    def __init__(
            self, repo: CourseWorkRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetCourseWorkListRequest) -> list[CourseWorkDomainEntity]:
        course_works = await self.repo.all(with_unique=True)
        course_works = [self.mapper.map(CourseWorkDomainEntity, i) for i in course_works]
        return course_works
