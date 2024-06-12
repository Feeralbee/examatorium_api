from didiator import Command
from pydantic import BaseModel

from domain.entities import ThemeDomainEntity


class GetThemeRequest(BaseModel, Command[ThemeDomainEntity]):
    id: str


class GetExamThemesRequest(BaseModel, Command[list[ThemeDomainEntity]]):
    exam_id: str


class GetThemeListRequest(BaseModel, Command[list[ThemeDomainEntity]]):
    pass
