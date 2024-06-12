from typing import Annotated

from didiator import Mediator
from fastapi import APIRouter, Depends

from application.dependencies import get_mediator
from domain.entities import GroupDomainEntity, GroupStudentDomainEntity
from domain.models.requests import group_students, GetStudentGroupRequest, DeleteGroupStudentByStudentIdRequest
from domain.models.requests import groups as groups_requests, GetGroupStudentListRequest

router = APIRouter(tags=["groups"])


@router.get("/groups/all")
async def all_groups(mediator: Annotated[Mediator, Depends(get_mediator)]) -> list[GroupDomainEntity]:
    request = groups_requests.GetGroupListRequest()
    response = await mediator.send(request)
    return response


@router.get("/groups/students")
async def all_groups_students(mediator: Annotated[Mediator, Depends(get_mediator)]) -> list[GroupStudentDomainEntity]:
    return await mediator.send(GetGroupStudentListRequest())


@router.get("/groups/student_group")
async def student_group(student_id: str,
                        mediator: Annotated[Mediator, Depends(get_mediator)]) -> GroupDomainEntity | None:
    group_student = await mediator.send(GetStudentGroupRequest(student_id=student_id))
    if group_student:
        return await mediator.send(groups_requests.GetGroupRequest(id=group_student.group_id))


@router.post("/groups/add_student")
async def add_student(
        group_id: str,
        student_id: str,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> GroupDomainEntity:
    await mediator.send(DeleteGroupStudentByStudentIdRequest(student_id=student_id))
    request = group_students.CreateGroupStudentRequest(group_id=group_id, student_id=student_id)
    group_student = await mediator.send(request)
    group = await mediator.send(groups_requests.GetGroupRequest(id=group_student.group_id))
    return group


@router.post("/groups/remove_student")
async def remove_student(
        student_id: str,
        mediator: Annotated[Mediator, Depends(get_mediator)]
):
    request = group_students.DeleteGroupStudentByStudentIdRequest(student_id=student_id)
    response = await mediator.send(request)
    return response


@router.get("/groups/{group_id}")
async def group(group_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]) -> GroupDomainEntity:
    request = groups_requests.GetGroupRequest(id=group_id)
    response = await mediator.send(request)
    if response:
        return response


@router.post("/groups")
async def create(
        data: groups_requests.CreateGroupRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> GroupDomainEntity:
    response = await mediator.send(data)
    return response


@router.patch("/groups")
async def update(
        data: groups_requests.UpdateGroupRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> GroupDomainEntity:
    response = await mediator.send(data)
    if response:
        return response


@router.delete("/groups/{group_id}")
async def delete(group_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]):
    return await mediator.send(groups_requests.DeleteGroupRequest(id=group_id))
