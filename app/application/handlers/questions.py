from typing import Annotated

from didiator import Mediator
from fastapi import APIRouter, Depends

from application.dependencies import get_mediator
from domain.entities import QuestionDomainEntity
from domain.models.requests import questions

router = APIRouter(tags=["questions"])


@router.get("/questions/all")
async def all(mediator: Annotated[Mediator, Depends(get_mediator)]) -> list[QuestionDomainEntity]:
    response = await mediator.send(questions.GetQuestionListRequest())
    return response


@router.get("/questions/{question_id}")
async def question(question_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]) -> QuestionDomainEntity:
    response = await mediator.send(questions.GetQuestionRequest(id=question_id))
    return response


@router.post("/questions")
async def create(
        data: questions.CreateQuestionRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> QuestionDomainEntity:
    response = await mediator.send(data)
    return response


@router.patch("/questions")
async def update(
        data: questions.UpdateQuestionRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> QuestionDomainEntity:
    response = await mediator.send(data)
    return response


@router.delete("/questions/{question_id}")
async def delete(question_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]):
    response = await mediator.send(questions.DeleteQuestionRequest(id=question_id))
    return response
