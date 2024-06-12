from datetime import datetime
from typing import Annotated

from didiator import Mediator
from docxtpl import DocxTemplate
from fastapi import APIRouter, Depends
from starlette.responses import FileResponse

from application.dependencies import get_mediator
from domain.entities import GraduateThesisDomainEntity
from domain.models.requests import graduate_theses, GetStudentGroupRequest, GetUserRequest

router = APIRouter(tags=["graduate_theses"])


@router.get("/graduate_theses/all")
async def all(mediator: Annotated[Mediator, Depends(get_mediator)]) -> list[GraduateThesisDomainEntity]:
    response = await mediator.send(graduate_theses.GetGraduateThesisListRequest())
    return response


@router.get("/graduate_theses/student")
async def student_graduate_theses(student_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]
                                  ) -> list[GraduateThesisDomainEntity]:
    group = await mediator.send(GetStudentGroupRequest(student_id=student_id))
    if not group:
        return []
    result = await mediator.send(graduate_theses.GetGraduateThesisListByGroupRequest(group_id=group.group_id))
    return result


@router.get("/graduate_theses/pages")
async def pages(student_id: str, graduate_thesis_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]):
    user = await mediator.send(GetUserRequest(id=student_id))
    graduate_thesis = await mediator.send(
        graduate_theses.GetGraduateThesisRequest(id=graduate_thesis_id))
    student_full_name = f"{user.surname} {user.name} {user.patronymic}"
    student_short_name = f"{user.surname} {user.name[0]}.{user.patronymic[0]}."
    if not user.patronymic:
        student_short_name = f"{user.surname} {user.name[0]}."
    doc = DocxTemplate("./application/docx/graduate_theses.docx")
    context = {
        "speciality": graduate_thesis.group.speciality,
        "group": graduate_thesis.group.name,
        "qualification": f"{graduate_thesis.group.qualification.index} {graduate_thesis.group.qualification.name}",
        "student_short_name": student_short_name,
        "student_full_name": student_full_name,
    }
    doc.render(context)
    file_name = f"{datetime.now()}.docx"
    doc.save(file_name)
    return FileResponse(path=file_name, filename="ВКР титульные листы.docx", media_type='multipart/form-data')


@router.get("/graduate_theses/{graduate_thesis_id}")
async def course_work(graduate_thesis_id: str,
                      mediator: Annotated[Mediator, Depends(get_mediator)]) -> GraduateThesisDomainEntity:
    response = await mediator.send(graduate_theses.GetGraduateThesisRequest(id=graduate_thesis_id))
    return response


@router.post("/graduate_theses")
async def create(
        data: graduate_theses.CreateGraduateThesisRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> GraduateThesisDomainEntity:
    response = await mediator.send(data)
    return response


@router.patch("/graduate_theses")
async def update(
        data: graduate_theses.UpdateGraduateThesisRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> GraduateThesisDomainEntity:
    response = await mediator.send(data)
    return response


@router.delete("/graduate_theses/{course_work_id}")
async def delete(graduate_thesis_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]):
    response = await mediator.send(graduate_theses.DeleteGraduateThesisRequest(id=graduate_thesis_id))
    return response
