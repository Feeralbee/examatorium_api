from didiator import Mediator
from fastapi import APIRouter, Depends

from application.dependencies import get_mediator
from application.exceptions import UserNotFoundException
from domain.entities import UserDomainEntity
from domain.models.requests import GetUserRequest, GetUserListRequest, CreateUserRequest, DeleteUserRequest, \
    UpdateUserRequest, GetUserByAuthorisationRequest, UpdateUserPasswordRequest

router = APIRouter(tags=["users"])


@router.get("/users/all")
async def get_all_users(mediator: Mediator = Depends(get_mediator)) -> list[UserDomainEntity]:
    request = GetUserListRequest()
    response = await mediator.send(request)
    return response


@router.get("/users/{user_id}")
async def get_user_by_id(user_id: str, mediator: Mediator = Depends(get_mediator)) -> UserDomainEntity:
    request = GetUserRequest(id=user_id)
    response = await mediator.send(request)
    if response:
        return response
    raise UserNotFoundException


@router.get("/users")
async def get_user_by_authorization(
        login: str,
        password: str,
        mediator: Mediator = Depends(get_mediator)) -> UserDomainEntity:
    request = GetUserByAuthorisationRequest(login=login, password=password)
    response = await mediator.send(request)
    if response:
        return response
    raise UserNotFoundException


@router.post("/users")
async def create_user(data: CreateUserRequest, mediator: Mediator = Depends(get_mediator)) -> UserDomainEntity:
    response = await mediator.send(data)
    return response


@router.delete("/users/{user_id}")
async def delete_user(user_id: str, mediator: Mediator = Depends(get_mediator)):
    request = DeleteUserRequest(id=user_id)
    response = await mediator.send(request)
    return response


@router.patch("/users")
async def update_user(
        data: UpdateUserRequest,
        mediator: Mediator = Depends(get_mediator)) -> UserDomainEntity:
    response = await mediator.send(data)
    return response


@router.patch("/users/password")
async def update_user_password(
        data: UpdateUserPasswordRequest,
        mediator: Mediator = Depends(get_mediator)) -> UserDomainEntity:
    response = await mediator.send(data)
    return response
