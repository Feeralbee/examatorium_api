from didiator import Command
from pydantic import BaseModel

from domain.entities import GraduateThesisDomainEntity


class GetGraduateThesisRequest(BaseModel, Command[GraduateThesisDomainEntity]):
    id: str


class GetGraduateThesisListByGroupRequest(BaseModel, Command[list[GraduateThesisDomainEntity]]):
    group_id: str


class GetGraduateThesisListRequest(BaseModel, Command[list[GraduateThesisDomainEntity]]):
    pass
