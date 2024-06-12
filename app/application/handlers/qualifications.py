from typing import Annotated

from didiator import Mediator
from fastapi import APIRouter, Depends

from application.dependencies import get_mediator
from domain.entities import QualificationDomainEntity
from domain.models.requests import qualifications, CreateQualificationCompetenceRequest, \
    GetQualCompetenciesByQualificationIdRequest, DeleteQualificationCompetenceRequest

router = APIRouter(tags=["qualifications"])


@router.get("/qualifications/all")
async def all(mediator: Annotated[Mediator, Depends(get_mediator)]) -> list[QualificationDomainEntity]:
    response = await mediator.send(qualifications.GetQualificationListRequest())
    return response


@router.get("/qualifications/{qualification_id}")
async def qualification(qualification_id: str,
                        mediator: Annotated[Mediator, Depends(get_mediator)]) -> QualificationDomainEntity:
    response = await mediator.send(qualifications.GetQualificationRequest(id=qualification_id))
    return response


@router.post("/qualifications")
async def create(
        data: qualifications.CreateQualificationRequest, competencies: list[str],
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> QualificationDomainEntity:
    qualification = await mediator.send(data)
    if qualification:
        for competence in competencies:
            await mediator.send(
                CreateQualificationCompetenceRequest(qualification_id=qualification.id, competence_id=competence))
        qualification = await mediator.send(qualifications.GetQualificationRequest(id=qualification.id))
        return qualification


@router.patch("/qualifications")
async def update(
        data: qualifications.UpdateQualificationRequest, competencies: list[str],
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> QualificationDomainEntity:
    qualifications_competencies = await mediator.send(
        GetQualCompetenciesByQualificationIdRequest(qualification_id=data.id))
    for qualification_competence in qualifications_competencies:
        await mediator.send(DeleteQualificationCompetenceRequest(id=qualification_competence.id))
    for competence in competencies:
        await mediator.send(
            CreateQualificationCompetenceRequest(qualification_id=data.id, competence_id=competence))
    response = await mediator.send(data)
    return response


@router.delete("/qualifications/{qualification_id}")
async def delete(qualification_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]):
    qualifications_competencies = await mediator.send(
        GetQualCompetenciesByQualificationIdRequest(qualification_id=qualification_id))
    for qualification_competence in qualifications_competencies:
        await mediator.send(DeleteQualificationCompetenceRequest(id=qualification_competence.id))
    response = await mediator.send(qualifications.DeleteQualificationRequest(id=qualification_id))
    return response
