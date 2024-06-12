import hashlib
from didiator import CommandHandler
from domain.entities import UserDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import UpdateUserRequest, UpdateUserPasswordRequest
from infrastructure.repositories import UserRepository


class UpdateUserHandler(CommandHandler[UpdateUserRequest, UserDomainEntity]):
    def __init__(
            self, repo: UserRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: UpdateUserRequest) -> UserDomainEntity:
        response = await self.repo.update(
            command.id,
            **command.model_dump(exclude={"id", }, exclude_unset=True)
        )
        return self.mapper.map(UserDomainEntity, response)


class UpdateUserPasswordHandler(CommandHandler[UpdateUserPasswordRequest, UserDomainEntity]):
    def __init__(
            self, repo: UserRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: UpdateUserPasswordRequest) -> UserDomainEntity:
        command.password = hashlib.md5(command.password.encode()).hexdigest()
        response = await self.repo.update(
            command.id,
            **command.model_dump(exclude={"id", }, exclude_unset=True)
        )
        return self.mapper.map(UserDomainEntity, response)
