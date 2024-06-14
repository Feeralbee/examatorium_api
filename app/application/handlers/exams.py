import datetime
import random
from typing import Annotated
from zipfile import ZipFile

from didiator import Mediator
from docxtpl import DocxTemplate
from fastapi import APIRouter, Depends
from loguru import logger
from starlette.responses import FileResponse

from application.dependencies import get_mediator
from domain.entities import ExamDomainEntity, QuestionDomainEntity, ThemeDomainEntity
from domain.models.requests import exams, GetExamListByTeacherRequest, GetStudentGroupRequest, \
    GetExamListByGroupRequest, GetExamRequest, GetExamThemesRequest
from domain.models.responses import QuestionsCount

router = APIRouter(tags=["exams"])


@router.get("/exams/all")
async def all(mediator: Annotated[Mediator, Depends(get_mediator)]) -> list[ExamDomainEntity]:
    response = await mediator.send(exams.GetExamListRequest())
    return response


@router.get("/exams/teacher")
async def teacher_exams(teacher_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]) -> list[ExamDomainEntity]:
    exams = await mediator.send(GetExamListByTeacherRequest(teacher_id=teacher_id))
    return exams


@router.get("/exams/student")
async def student_exams(student_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]) -> list[ExamDomainEntity]:
    group = await mediator.send(GetStudentGroupRequest(student_id=student_id))
    if not group:
        return []
    exams = await mediator.send(GetExamListByGroupRequest(group_id=group.group_id))
    return exams


@router.get("/exams/questions")
async def exam_questions(exam_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]) -> list[ThemeDomainEntity]:
    return await mediator.send(GetExamThemesRequest(exam_id=exam_id))


@router.get("/exams/questions_count")
async def get(exam_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]) -> QuestionsCount:
    exam_themes = await mediator.send(GetExamThemesRequest(exam_id=exam_id))
    questions: list[QuestionDomainEntity] = []
    for theme in exam_themes:
        questions += theme.questions
    task_questions = [question.name for question in questions if question.is_task_question]
    return QuestionsCount(all=len(questions), task_questions=len(task_questions))


@router.get("/exams/tickets")
async def tickets(
        exam_id: str,
        tickets_count: int,
        questions_count: int,
        task_questions_count: int,
        mediator: Annotated[Mediator, Depends(get_mediator)]
):
    exam = await mediator.send(GetExamRequest(id=exam_id))
    exam_themes = await mediator.send(GetExamThemesRequest(exam_id=exam_id))
    questions: list[QuestionDomainEntity] = []
    for theme in exam_themes:
        questions += theme.questions
    task_questions = [question.name for question in questions if question.is_task_question]
    not_task_questions = [question.name for question in questions if not question.is_task_question]
    folder_name = str(datetime.datetime.now())
    short_name = f"{exam.teacher.surname} {exam.teacher.name[0]}."
    if exam.teacher.patronymic:
        short_name = f"{exam.teacher.surname} {exam.teacher.name[0]}.{exam.teacher.patronymic[0]}."
    for i in range(0, tickets_count):
        logger.info(i)
        doc = DocxTemplate("./application/docx/ticket.docx")
        ticket_questions = ""
        if questions_count == task_questions_count:
            for index, x in enumerate(random.sample(task_questions, task_questions_count)):
                ticket_questions += f"{index+1}. {x}\n"
        elif task_questions_count == 0:
            for index, x in enumerate(random.sample(not_task_questions, questions_count)):
                ticket_questions += f"{index+1}. {x}\n"
        else:
            for index, x in enumerate(random.sample(not_task_questions, questions_count-task_questions_count)):
                ticket_questions += f"{index+1}. {x}\n"
            for index, x in enumerate(random.sample(task_questions, task_questions_count)):
                ticket_questions += f"{index+1+questions_count-task_questions_count}. {x}\n"
        context = {
            "group": exam.group.name,
            "discipline": f"{exam.discipline.index} {exam.discipline.name}",
            "semester": exam.semester,
            "short_name": short_name,
            "questions": ticket_questions,
            "i": i+1,
        }
        doc.render(context)
        doc_name = f"Билет {i+1}.docx"
        doc.save(doc_name)
    with ZipFile(f"./{folder_name}.zip", "w") as zip_object:
        for i in range(0, tickets_count):
            doc_name = f"Билет {i+1}.docx"
            zip_object.write(doc_name)

    return FileResponse(path=f"{folder_name}.zip", filename="Билеты.zip", media_type='multipart/form-data')


@router.get("/exams/{exam_id}")
async def exam(exam_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]) -> ExamDomainEntity:
    response = await mediator.send(exams.GetExamRequest(id=exam_id))
    return response


@router.post("/exams")
async def create(
        data: exams.CreateExamRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> ExamDomainEntity:
    response = await mediator.send(data)
    return response


@router.patch("/exams")
async def update(
        data: exams.UpdateExamRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> ExamDomainEntity:
    response = await mediator.send(data)
    return response


@router.delete("/exams/{exam_id}")
async def delete(exam_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]):
    response = await mediator.send(exams.DeleteExamRequest(id=exam_id))
    return response
