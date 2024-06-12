import hashlib
from didiator import CommandHandler

from domain.entities import UserDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import GetUserRequest, GetUserListRequest, GetUserByAuthorisationRequest
from infrastructure.repositories import UserRepository


class GetUserHandler(CommandHandler[GetUserRequest, UserDomainEntity]):
    def __init__(
            self, repo: UserRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetUserRequest) -> UserDomainEntity | None:
        response = await self.repo.get(command.id)
        if response:
            return self.mapper.map(UserDomainEntity, response)


class GetUserByAuthorizationHandler(CommandHandler[GetUserByAuthorisationRequest, UserDomainEntity]):
    def __init__(
            self, repo: UserRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetUserRequest) -> UserDomainEntity | None:
        password_hash = hashlib.md5(command.password.encode()).hexdigest()
        response = await self.repo.get_by(login=command.login, password=password_hash)
        if response:
            return self.mapper.map(UserDomainEntity, response)


class GetUserListHandler(CommandHandler[GetUserListRequest, list[UserDomainEntity]]):
    def __init__(
            self, repo: UserRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetUserListRequest) -> list[UserDomainEntity]:
        users = await self.repo.all(with_unique=True)
        user_list = [self.mapper.map(UserDomainEntity, i) for i in users]
        return user_list
