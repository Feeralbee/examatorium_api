import logging
from contextlib import asynccontextmanager
from functools import partial

import sentry_sdk
from di import Container, bind_by_type
from di.api.providers import DependencyProviderType
from di.api.scopes import Scope
from di.dependent import Dependent
from di.executors import AsyncExecutor
from didiator import CommandDispatcherImpl, MediatorImpl, QueryDispatcherImpl, EventObserverImpl, Mediator, \
    QueryMediator, CommandMediator, EventMediator
from didiator.interface.utils.di_builder import DiBuilder
from didiator.middlewares.di import DiMiddleware, DiScopes
from didiator.middlewares.logging import LoggingMiddleware
from didiator.utils.di_builder import DiBuilderImpl
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from starlette.middleware.cors import CORSMiddleware

from application import handlers
from application.constants import DIScopes
from application.dependencies import build_sa_session, get_di_state, get_mediator
from application.dependencies.mediator import get_di_builder
from application.exceptions import UserNotFoundException, user_not_found_handler
from application.mediator import StateProvider, MediatorProvider
from config import Config
from domain import handlers as domain_handlers
from domain.entities import (UserDomainEntity, GroupDomainEntity, QuestionDomainEntity, QualificationDomainEntity,
                             ThemeDomainEntity, CompetenceDomainEntity, DisciplineDomainEntity, ExamDomainEntity,
                             GroupStudentDomainEntity,
                             QualificationCompetenceDomainEntity, GraduateThesisDomainEntity, CourseWorkDomainEntity,
                             EducationalPracticeDomainEntity, )
from domain.mapping import ClassMapper, MappingConfiguration, IClassMapper
from domain.mapping.mappers import MTPMapper, PTMMapper
from domain.models import requests as domain_requests
from infrastructure.entities import (UserModel, GroupModel, QuestionModel, ExamModel, CompetenceModel, DisciplineModel,
                                     QualificationModel, ThemeModel,
                                     GroupStudentModel, QualificationCompetenceModel, GraduateThesisModel,
                                     CourseWorkModel, EducationalPracticeModel, )
from infrastructure.repositories import (UserRepository, )


def setup_mapper_configuration() -> MappingConfiguration:
    mapping_configuration = MappingConfiguration()

    # <------ Models -> Entities ------>

    mapping_configuration.add_mapper(
        from_cls=UserModel, to_cls=UserDomainEntity,
        mapper=MTPMapper[UserModel, UserDomainEntity]()
    )
    mapping_configuration.add_mapper(
        from_cls=GroupModel, to_cls=GroupDomainEntity,
        mapper=MTPMapper[GroupModel, GroupDomainEntity]()
    )

    mapping_configuration.add_mapper(
        from_cls=QuestionModel, to_cls=QuestionDomainEntity,
        mapper=MTPMapper[QuestionModel, QuestionDomainEntity]()
    )

    mapping_configuration.add_mapper(
        from_cls=DisciplineModel, to_cls=DisciplineDomainEntity,
        mapper=MTPMapper[DisciplineModel, DisciplineDomainEntity]()
    )

    mapping_configuration.add_mapper(
        from_cls=ThemeModel, to_cls=ThemeDomainEntity,
        mapper=MTPMapper[ThemeModel, ThemeDomainEntity]()
    )

    mapping_configuration.add_mapper(
        from_cls=ExamModel, to_cls=ExamDomainEntity,
        mapper=MTPMapper[ExamModel, ExamDomainEntity]()
    )

    mapping_configuration.add_mapper(
        from_cls=QualificationModel, to_cls=QualificationDomainEntity,
        mapper=MTPMapper[QualificationModel, QualificationDomainEntity]()
    )

    mapping_configuration.add_mapper(
        from_cls=CompetenceModel, to_cls=CompetenceDomainEntity,
        mapper=MTPMapper[CompetenceModel, CompetenceDomainEntity]()
    )

    mapping_configuration.add_mapper(
        from_cls=GroupStudentModel, to_cls=GroupStudentDomainEntity,
        mapper=MTPMapper[GroupStudentModel, GroupStudentDomainEntity]()
    )

    mapping_configuration.add_mapper(
        from_cls=QualificationCompetenceModel, to_cls=QualificationCompetenceDomainEntity,
        mapper=MTPMapper[QualificationCompetenceModel, QualificationCompetenceDomainEntity]()
    )

    mapping_configuration.add_mapper(
        from_cls=GraduateThesisModel, to_cls=GraduateThesisDomainEntity,
        mapper=MTPMapper[GraduateThesisModel, GraduateThesisDomainEntity]()
    )

    mapping_configuration.add_mapper(
        from_cls=CourseWorkModel, to_cls=CourseWorkDomainEntity,
        mapper=MTPMapper[CourseWorkModel, CourseWorkDomainEntity]()
    )

    mapping_configuration.add_mapper(
        from_cls=EducationalPracticeModel, to_cls=EducationalPracticeDomainEntity,
        mapper=MTPMapper[EducationalPracticeModel, EducationalPracticeDomainEntity]()
    )

    # <------ Requests ------>

    # USERS

    mapping_configuration.add_mapper(
        from_cls=domain_requests.users.CreateUserRequest, to_cls=UserModel,
        mapper=PTMMapper[domain_requests.users.CreateUserRequest, UserModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.users.UpdateUserRequest, to_cls=UserModel,
        mapper=PTMMapper[domain_requests.users.UpdateUserRequest, UserModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.users.UpdateUserPasswordRequest, to_cls=UserModel,
        mapper=PTMMapper[domain_requests.users.UpdateUserPasswordRequest, UserModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.users.DeleteUserRequest, to_cls=UserModel,
        mapper=PTMMapper[domain_requests.users.DeleteUserRequest, UserModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.users.GetUserRequest, to_cls=UserModel,
        mapper=PTMMapper[domain_requests.users.GetUserRequest, UserModel]()
    )

    # GROUPS

    mapping_configuration.add_mapper(
        from_cls=domain_requests.groups.GetGroupRequest, to_cls=GroupModel,
        mapper=PTMMapper[domain_requests.groups.GetGroupRequest, GroupModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.groups.UpdateGroupRequest, to_cls=GroupModel,
        mapper=PTMMapper[domain_requests.groups.UpdateGroupRequest, GroupModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.groups.DeleteGroupRequest, to_cls=GroupModel,
        mapper=PTMMapper[domain_requests.groups.DeleteGroupRequest, GroupModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.groups.CreateGroupRequest, to_cls=GroupModel,
        mapper=PTMMapper[domain_requests.groups.CreateGroupRequest, GroupModel]()
    )

    # DISCIPLINES

    mapping_configuration.add_mapper(
        from_cls=domain_requests.disciplines.GetDisciplineRequest, to_cls=DisciplineModel,
        mapper=PTMMapper[domain_requests.disciplines.GetDisciplineRequest, DisciplineModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.disciplines.UpdateDisciplineRequest, to_cls=DisciplineModel,
        mapper=PTMMapper[domain_requests.disciplines.UpdateDisciplineRequest, DisciplineModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.disciplines.DeleteDisciplineRequest, to_cls=DisciplineModel,
        mapper=PTMMapper[domain_requests.disciplines.DeleteDisciplineRequest, DisciplineModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.disciplines.CreateDisciplineRequest, to_cls=DisciplineModel,
        mapper=PTMMapper[domain_requests.disciplines.CreateDisciplineRequest, DisciplineModel]()
    )

    # THEMES

    mapping_configuration.add_mapper(
        from_cls=domain_requests.themes.GetThemeRequest, to_cls=ThemeModel,
        mapper=PTMMapper[domain_requests.themes.GetThemeRequest, ThemeModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.themes.UpdateThemeRequest, to_cls=ThemeModel,
        mapper=PTMMapper[domain_requests.themes.UpdateThemeRequest, ThemeModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.themes.DeleteThemeRequest, to_cls=ThemeModel,
        mapper=PTMMapper[domain_requests.themes.DeleteThemeRequest, ThemeModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.themes.CreateThemeRequest, to_cls=ThemeModel,
        mapper=PTMMapper[domain_requests.themes.CreateThemeRequest, ThemeModel]()
    )

    # QUESTIONS

    mapping_configuration.add_mapper(
        from_cls=domain_requests.questions.GetQuestionRequest, to_cls=QuestionModel,
        mapper=PTMMapper[domain_requests.questions.GetQuestionRequest, QuestionModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.questions.UpdateQuestionRequest, to_cls=QuestionModel,
        mapper=PTMMapper[domain_requests.questions.UpdateQuestionRequest, QuestionModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.questions.DeleteQuestionRequest, to_cls=QuestionModel,
        mapper=PTMMapper[domain_requests.questions.DeleteQuestionRequest, QuestionModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.questions.CreateQuestionRequest, to_cls=QuestionModel,
        mapper=PTMMapper[domain_requests.questions.CreateQuestionRequest, QuestionModel]()
    )

    # EXAMS

    mapping_configuration.add_mapper(
        from_cls=domain_requests.exams.GetExamRequest, to_cls=ExamModel,
        mapper=PTMMapper[domain_requests.exams.GetExamRequest, ExamModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.exams.UpdateExamRequest, to_cls=ExamModel,
        mapper=PTMMapper[domain_requests.exams.UpdateExamRequest, ExamModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.exams.DeleteExamRequest, to_cls=ExamModel,
        mapper=PTMMapper[domain_requests.exams.DeleteExamRequest, ExamModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.exams.CreateExamRequest, to_cls=ExamModel,
        mapper=PTMMapper[domain_requests.exams.CreateExamRequest, ExamModel]()
    )

    # COURSE WORKS

    mapping_configuration.add_mapper(
        from_cls=domain_requests.course_works.GetCourseWorkRequest, to_cls=CourseWorkModel,
        mapper=PTMMapper[domain_requests.course_works.GetCourseWorkRequest, CourseWorkModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.course_works.UpdateCourseWorkRequest, to_cls=CourseWorkModel,
        mapper=PTMMapper[domain_requests.course_works.UpdateCourseWorkRequest, CourseWorkModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.course_works.DeleteCourseWorkRequest, to_cls=CourseWorkModel,
        mapper=PTMMapper[domain_requests.course_works.DeleteCourseWorkRequest, CourseWorkModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.course_works.CreateCourseWorkRequest, to_cls=CourseWorkModel,
        mapper=PTMMapper[domain_requests.course_works.CreateCourseWorkRequest, CourseWorkModel]()
    )

    # GRADUATE THESES

    mapping_configuration.add_mapper(
        from_cls=domain_requests.graduate_theses.GetGraduateThesisRequest, to_cls=GraduateThesisModel,
        mapper=PTMMapper[domain_requests.graduate_theses.GetGraduateThesisRequest, GraduateThesisModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.graduate_theses.UpdateGraduateThesisRequest, to_cls=GraduateThesisModel,
        mapper=PTMMapper[domain_requests.graduate_theses.UpdateGraduateThesisRequest, GraduateThesisModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.graduate_theses.DeleteGraduateThesisRequest, to_cls=GraduateThesisModel,
        mapper=PTMMapper[domain_requests.graduate_theses.DeleteGraduateThesisRequest, GraduateThesisModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.graduate_theses.CreateGraduateThesisRequest, to_cls=GraduateThesisModel,
        mapper=PTMMapper[domain_requests.graduate_theses.CreateGraduateThesisRequest, GraduateThesisModel]()
    )

    # educational practices

    mapping_configuration.add_mapper(
        from_cls=domain_requests.educational_practices.GetEducationalPracticeRequest, to_cls=EducationalPracticeModel,
        mapper=PTMMapper[
            domain_requests.educational_practices.GetEducationalPracticeRequest, EducationalPracticeModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.educational_practices.UpdateEducationalPracticeRequest,
        to_cls=EducationalPracticeModel,
        mapper=PTMMapper[
            domain_requests.educational_practices.UpdateEducationalPracticeRequest, EducationalPracticeModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.educational_practices.DeleteEducationalPracticeRequest,
        to_cls=EducationalPracticeModel,
        mapper=PTMMapper[
            domain_requests.educational_practices.DeleteEducationalPracticeRequest, EducationalPracticeModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.educational_practices.CreateEducationalPracticeRequest,
        to_cls=EducationalPracticeModel,
        mapper=PTMMapper[
            domain_requests.educational_practices.CreateEducationalPracticeRequest, EducationalPracticeModel]()
    )

    # QUALIFICATIONS

    mapping_configuration.add_mapper(
        from_cls=domain_requests.qualifications.GetQualificationRequest, to_cls=QualificationModel,
        mapper=PTMMapper[domain_requests.qualifications.GetQualificationRequest, QualificationModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.qualifications.UpdateQualificationRequest, to_cls=QualificationModel,
        mapper=PTMMapper[domain_requests.qualifications.UpdateQualificationRequest, QualificationModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.qualifications.CreateQualificationRequest, to_cls=QualificationModel,
        mapper=PTMMapper[domain_requests.qualifications.CreateQualificationRequest, QualificationModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.qualifications.DeleteQualificationRequest, to_cls=QualificationModel,
        mapper=PTMMapper[domain_requests.qualifications.DeleteQualificationRequest, QualificationModel]()
    )

    # COMPETENCIES

    mapping_configuration.add_mapper(
        from_cls=domain_requests.competencies.GetCompetenceRequest, to_cls=CompetenceModel,
        mapper=PTMMapper[domain_requests.competencies.GetCompetenceRequest, CompetenceModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.competencies.UpdateCompetenceRequest, to_cls=CompetenceModel,
        mapper=PTMMapper[domain_requests.competencies.UpdateCompetenceRequest, CompetenceModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.competencies.CreateCompetenceRequest, to_cls=CompetenceModel,
        mapper=PTMMapper[domain_requests.competencies.CreateCompetenceRequest, CompetenceModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.competencies.DeleteCompetenceRequest, to_cls=CompetenceModel,
        mapper=PTMMapper[domain_requests.competencies.DeleteCompetenceRequest, CompetenceModel]()
    )

    # GROUP STUDENT

    mapping_configuration.add_mapper(
        from_cls=domain_requests.group_students.DeleteGroupStudentRequest, to_cls=GroupStudentModel,
        mapper=PTMMapper[domain_requests.group_students.DeleteGroupStudentRequest, GroupStudentModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.group_students.CreateGroupStudentRequest, to_cls=GroupStudentModel,
        mapper=PTMMapper[domain_requests.group_students.CreateGroupStudentRequest, GroupStudentModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.group_students.GetGroupStudentRequest, to_cls=GroupStudentModel,
        mapper=PTMMapper[domain_requests.group_students.GetGroupStudentRequest, GroupStudentModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.group_students.DeleteGroupStudentByStudentIdRequest, to_cls=GroupStudentModel,
        mapper=PTMMapper[domain_requests.group_students.DeleteGroupStudentByStudentIdRequest, GroupStudentModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.group_students.GetStudentGroupRequest, to_cls=GroupStudentModel,
        mapper=PTMMapper[domain_requests.group_students.GetStudentGroupRequest, GroupStudentModel]()
    )

    # QUALIFICATION COMPETENCE

    mapping_configuration.add_mapper(
        from_cls=domain_requests.CreateQualificationCompetenceRequest, to_cls=QualificationCompetenceModel,
        mapper=PTMMapper[domain_requests.CreateQualificationCompetenceRequest, QualificationCompetenceModel]()
    )

    mapping_configuration.add_mapper(
        from_cls=domain_requests.DeleteQualificationCompetenceRequest, to_cls=QualificationCompetenceModel,
        mapper=PTMMapper[domain_requests.DeleteQualificationCompetenceRequest, QualificationCompetenceModel]()
    )

    return mapping_configuration


def init_di_builder() -> DiBuilder:
    di_container = Container()
    di_executor = AsyncExecutor()
    di_scopes = [DIScopes.app, DIScopes.request]
    di_builder = DiBuilderImpl(di_container, di_executor, di_scopes=di_scopes)
    return di_builder


def setup_mediator_factory(
        di_builder: DiBuilder,
        mediator_factory: DependencyProviderType,
        scope: Scope,
) -> None:
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), Mediator))
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), QueryMediator))
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), CommandMediator))
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), EventMediator))


def setup_di_builder(engine: AsyncEngine):
    di_builder = init_di_builder()

    mapping_configuration = setup_mapper_configuration()
    mapper = ClassMapper(config=mapping_configuration)

    di_builder.bind(bind_by_type(Dependent(lambda *args: di_builder, scope=DIScopes.app), DiBuilder))
    di_builder.bind(bind_by_type(Dependent(lambda *args: mapper, scope=DIScopes.app), IClassMapper))
    di_builder.bind(bind_by_type(Dependent(lambda *args: engine, scope=DIScopes.app), AsyncEngine))

    di_builder.bind(bind_by_type(Dependent(build_sa_session, scope=DIScopes.request), AsyncSession))

    di_builder.bind(bind_by_type(Dependent(UserRepository, scope=DIScopes.request), UserRepository))
    setup_mediator_factory(di_builder, get_mediator, DIScopes.request)
    return di_builder


def setup_mediator(mediator: Mediator):
    # USERS
    mediator.register_command_handler(domain_requests.users.GetUserRequest, domain_handlers.users.GetUserHandler)
    mediator.register_command_handler(domain_requests.users.CreateUserRequest, domain_handlers.users.CreateUserHandler)
    mediator.register_command_handler(domain_requests.users.UpdateUserRequest, domain_handlers.users.UpdateUserHandler)
    mediator.register_command_handler(domain_requests.users.UpdateUserPasswordRequest,
                                      domain_handlers.users.UpdateUserPasswordHandler)
    mediator.register_command_handler(domain_requests.users.DeleteUserRequest, domain_handlers.users.DeleteUserHandler)
    mediator.register_command_handler(domain_requests.users.GetUserListRequest,
                                      domain_handlers.users.GetUserListHandler)
    mediator.register_command_handler(domain_requests.users.GetUserByAuthorisationRequest,
                                      domain_handlers.users.GetUserByAuthorizationHandler)

    # GROUPS
    mediator.register_command_handler(
        domain_requests.groups.GetGroupRequest,
        domain_handlers.groups.GetGroupHandler
    )
    mediator.register_command_handler(
        domain_requests.groups.GetGroupListRequest,
        domain_handlers.groups.GetGroupListHandler
    )
    mediator.register_command_handler(
        domain_requests.groups.UpdateGroupRequest,
        domain_handlers.groups.UpdateGroupHandler,
    )
    mediator.register_command_handler(
        domain_requests.groups.CreateGroupRequest,
        domain_handlers.groups.CreateGroupHandler,
    )
    mediator.register_command_handler(
        domain_requests.groups.DeleteGroupRequest,
        domain_handlers.groups.DeleteGroupHandler,
    )

    # DISCIPLINES
    mediator.register_command_handler(
        domain_requests.disciplines.GetDisciplineRequest,
        domain_handlers.disciplines.GetDisciplineHandler,
    )
    mediator.register_command_handler(
        domain_requests.disciplines.GetDisciplineListRequest,
        domain_handlers.disciplines.GetDisciplineListHandler,
    )
    mediator.register_command_handler(
        domain_requests.disciplines.UpdateDisciplineRequest,
        domain_handlers.disciplines.UpdateDisciplineHandler,
    )
    mediator.register_command_handler(
        domain_requests.disciplines.CreateDisciplineRequest,
        domain_handlers.disciplines.CreateDisciplineHandler,
    )
    mediator.register_command_handler(
        domain_requests.disciplines.DeleteDisciplineRequest,
        domain_handlers.disciplines.DeleteDisciplineHandler,
    )

    # THEMES
    mediator.register_command_handler(
        domain_requests.themes.GetThemeRequest,
        domain_handlers.themes.GetThemeHandler,
    )
    mediator.register_command_handler(
        domain_requests.themes.GetThemeListRequest,
        domain_handlers.themes.GetThemeListHandler,
    )
    mediator.register_command_handler(
        domain_requests.themes.UpdateThemeRequest,
        domain_handlers.themes.UpdateThemeHandler,
    )
    mediator.register_command_handler(
        domain_requests.themes.CreateThemeRequest,
        domain_handlers.themes.CreateThemeHandler,
    )
    mediator.register_command_handler(
        domain_requests.themes.DeleteThemeRequest,
        domain_handlers.themes.DeleteThemeHandler,
    )
    mediator.register_command_handler(
        domain_requests.themes.GetExamThemesRequest,
        domain_handlers.themes.GetExamThemesHandler,
    )

    # QUESTIONS
    mediator.register_command_handler(
        domain_requests.questions.GetQuestionRequest,
        domain_handlers.questions.GetQuestionHandler,
    )
    mediator.register_command_handler(
        domain_requests.questions.GetQuestionListRequest,
        domain_handlers.questions.GetQuestionListHandler,
    )
    mediator.register_command_handler(
        domain_requests.questions.UpdateQuestionRequest,
        domain_handlers.questions.UpdateQuestionHandler,
    )
    mediator.register_command_handler(
        domain_requests.questions.CreateQuestionRequest,
        domain_handlers.questions.CreateQuestionHandler,
    )
    mediator.register_command_handler(
        domain_requests.questions.DeleteQuestionRequest,
        domain_handlers.questions.DeleteQuestionHandler,
    )

    # EXAMS
    mediator.register_command_handler(
        domain_requests.exams.GetExamRequest,
        domain_handlers.exams.GetExamHandler,
    )
    mediator.register_command_handler(
        domain_requests.exams.GetExamListRequest,
        domain_handlers.exams.GetExamListHandler,
    )
    mediator.register_command_handler(
        domain_requests.exams.UpdateExamRequest,
        domain_handlers.exams.UpdateExamHandler,
    )
    mediator.register_command_handler(
        domain_requests.exams.CreateExamRequest,
        domain_handlers.exams.CreateExamHandler,
    )
    mediator.register_command_handler(
        domain_requests.exams.DeleteExamRequest,
        domain_handlers.exams.DeleteExamHandler,
    )
    mediator.register_command_handler(
        domain_requests.exams.GetExamListByRequest,
        domain_handlers.exams.GetExamListByHandler,
    )
    mediator.register_command_handler(
        domain_requests.exams.GetExamListByTeacherRequest,
        domain_handlers.exams.GetExamListByTeacherHandler,
    )
    mediator.register_command_handler(
        domain_requests.exams.GetExamListByGroupRequest,
        domain_handlers.exams.GetExamListByGroupHandler,
    )

    # GRADUATE THESES
    mediator.register_command_handler(
        domain_requests.graduate_theses.GetGraduateThesisRequest,
        domain_handlers.graduate_theses.GetGraduateThesisHandler,
    )
    mediator.register_command_handler(
        domain_requests.graduate_theses.GetGraduateThesisListRequest,
        domain_handlers.graduate_theses.GetGraduateThesisListHandler,
    )
    mediator.register_command_handler(
        domain_requests.graduate_theses.UpdateGraduateThesisRequest,
        domain_handlers.graduate_theses.UpdateGraduateThesisHandler,
    )
    mediator.register_command_handler(
        domain_requests.graduate_theses.CreateGraduateThesisRequest,
        domain_handlers.graduate_theses.CreateGraduateThesisHandler,
    )
    mediator.register_command_handler(
        domain_requests.graduate_theses.DeleteGraduateThesisRequest,
        domain_handlers.graduate_theses.DeleteGraduateThesisHandler,
    )
    mediator.register_command_handler(
        domain_requests.graduate_theses.GetGraduateThesisListByGroupRequest,
        domain_handlers.graduate_theses.GetGraduateThesisListByGroupHandler,
    )

    # Educational Practices
    mediator.register_command_handler(
        domain_requests.educational_practices.GetEducationalPracticeRequest,
        domain_handlers.educational_practices.GetEducationalPracticeHandler,
    )
    mediator.register_command_handler(
        domain_requests.educational_practices.GetEducationalPracticeListRequest,
        domain_handlers.educational_practices.GetEducationalPracticeListHandler,
    )
    mediator.register_command_handler(
        domain_requests.educational_practices.UpdateEducationalPracticeRequest,
        domain_handlers.educational_practices.UpdateEducationalPracticeHandler,
    )
    mediator.register_command_handler(
        domain_requests.educational_practices.CreateEducationalPracticeRequest,
        domain_handlers.educational_practices.CreateEducationalPracticeHandler,
    )
    mediator.register_command_handler(
        domain_requests.educational_practices.DeleteEducationalPracticeRequest,
        domain_handlers.educational_practices.DeleteEducationalPracticeHandler,
    )
    mediator.register_command_handler(
        domain_requests.educational_practices.GetEducationalPracticeListByGroupRequest,
        domain_handlers.educational_practices.GetEducationalPracticeListByGroupHandler,
    )

    # COURSE WORKS
    mediator.register_command_handler(
        domain_requests.course_works.GetCourseWorkRequest,
        domain_handlers.course_works.GetCourseWorkHandler,
    )
    mediator.register_command_handler(
        domain_requests.course_works.GetCourseWorkListRequest,
        domain_handlers.course_works.GetCourseWorkListHandler,
    )
    mediator.register_command_handler(
        domain_requests.course_works.UpdateCourseWorkRequest,
        domain_handlers.course_works.UpdateCourseWorkHandler,
    )
    mediator.register_command_handler(
        domain_requests.course_works.CreateCourseWorkRequest,
        domain_handlers.course_works.CreateCourseWorkHandler,
    )
    mediator.register_command_handler(
        domain_requests.course_works.DeleteCourseWorkRequest,
        domain_handlers.course_works.DeleteCourseWorkHandler,
    )
    mediator.register_command_handler(
        domain_requests.course_works.GetCourseWorkListByGroupRequest,
        domain_handlers.course_works.GetCourseWorkListByGroupHandler,
    )

    # QUALIFICATIONS
    mediator.register_command_handler(
        domain_requests.qualifications.GetQualificationRequest,
        domain_handlers.qualifications.GetQualificationHandler,
    )
    mediator.register_command_handler(
        domain_requests.qualifications.GetQualificationListRequest,
        domain_handlers.qualifications.GetQualificationListHandler,
    )
    mediator.register_command_handler(
        domain_requests.qualifications.UpdateQualificationRequest,
        domain_handlers.qualifications.UpdateQualificationHandler,
    )
    mediator.register_command_handler(
        domain_requests.qualifications.CreateQualificationRequest,
        domain_handlers.qualifications.CreateQualificationHandler,
    )
    mediator.register_command_handler(
        domain_requests.qualifications.DeleteQualificationRequest,
        domain_handlers.qualifications.DeleteQualificationHandler,
    )

    # COMPETENCIES
    mediator.register_command_handler(
        domain_requests.competencies.GetCompetenceRequest,
        domain_handlers.competencies.GetCompetenceHandler,
    )
    mediator.register_command_handler(
        domain_requests.competencies.GetCompetenceListRequest,
        domain_handlers.competencies.GetCompetenceListHandler,
    )
    mediator.register_command_handler(
        domain_requests.competencies.UpdateCompetenceRequest,
        domain_handlers.competencies.UpdateCompetenceHandler,
    )
    mediator.register_command_handler(
        domain_requests.competencies.CreateCompetenceRequest,
        domain_handlers.competencies.CreateCompetenceHandler,
    )
    mediator.register_command_handler(
        domain_requests.competencies.DeleteCompetenceRequest,
        domain_handlers.competencies.DeleteCompetenceHandler,
    )

    # GROUP STUDENTS
    mediator.register_command_handler(
        domain_requests.group_students.GetGroupStudentRequest,
        domain_handlers.group_students.GetGroupStudentHandler,
    )
    mediator.register_command_handler(
        domain_requests.group_students.CreateGroupStudentRequest,
        domain_handlers.group_students.CreateGroupStudentHandler,
    )
    mediator.register_command_handler(
        domain_requests.group_students.DeleteGroupStudentRequest,
        domain_handlers.group_students.DeleteGroupStudentHandler,
    )
    mediator.register_command_handler(
        domain_requests.group_students.DeleteGroupStudentByStudentIdRequest,
        domain_handlers.group_students.DeleteGroupStudentByStudentIdHandler,
    )
    mediator.register_command_handler(
        domain_requests.group_students.GetGroupStudentListRequest,
        domain_handlers.group_students.GetGroupStudentListHandler,
    )
    mediator.register_command_handler(
        domain_requests.group_students.GetStudentGroupRequest,
        domain_handlers.group_students.GetStudentGroupHandler,
    )

    # QUALIFICATION COMPETENCE
    mediator.register_command_handler(
        domain_requests.qualification_competencies.CreateQualificationCompetenceRequest,
        domain_handlers.qualification_competencies.CreateQualificationCompetenceHandler,
    )
    mediator.register_command_handler(
        domain_requests.qualification_competencies.GetQualCompetenciesByCompetenceIdRequest,
        domain_handlers.qualification_competencies.GetQualCompetenciesByCompetenceIdHandler,
    )
    mediator.register_command_handler(
        domain_requests.qualification_competencies.DeleteQualificationCompetenceRequest,
        domain_handlers.qualification_competencies.DeleteQualificationCompetenceHandler,
    )
    mediator.register_command_handler(
        domain_requests.qualification_competencies.GetQualCompetenciesByQualificationIdRequest,
        domain_handlers.qualification_competencies.GetQualCompetenciesByQualificationIdHandler,
    )


def init_mediator(di_builder: DiBuilder) -> Mediator:
    middlewares = (
        LoggingMiddleware("mediator", level=logging.DEBUG),
        DiMiddleware(di_builder, scopes=DiScopes(DIScopes.request)),
    )
    command_dispatcher = CommandDispatcherImpl(middlewares=middlewares)
    query_dispatcher = QueryDispatcherImpl(middlewares=middlewares)
    event_observer = EventObserverImpl(middlewares=middlewares)

    mediator = MediatorImpl(command_dispatcher, query_dispatcher, event_observer)
    return mediator


@asynccontextmanager
async def lifespan(di_builder: DiBuilderImpl, app: FastAPI):
    async with di_builder.enter_scope(DIScopes.app) as di_state:
        mediator = await di_builder.execute(init_mediator, DIScopes.app, state=di_state)
        setup_mediator(mediator)

        mediator_provider = MediatorProvider(mediator)

        app.dependency_overrides[get_mediator] = mediator_provider.build

        state_provider = StateProvider(di_state)

        app.dependency_overrides[get_di_builder] = lambda: di_builder
        app.dependency_overrides[get_di_state] = state_provider.build
        yield


def setup_routers(app: FastAPI):
    app.include_router(handlers.users_router)
    app.include_router(handlers.themes_router)
    app.include_router(handlers.exams_router)
    app.include_router(handlers.groups_router)
    app.include_router(handlers.questions_router)
    app.include_router(handlers.competencies_router)
    app.include_router(handlers.disciplines_router)
    app.include_router(handlers.qualifications_router)
    app.include_router(handlers.educational_practices_router)
    app.include_router(handlers.graduate_theses_router)
    app.include_router(handlers.course_works_router)

    return app


def setup_exceptions(app: FastAPI):
    app.add_exception_handler(UserNotFoundException, user_not_found_handler)

    return app


def setup_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


def main():
    sentry_sdk.init(Config.SENTRY_URL, traces_sample_rate=1.0, profiles_sample_rate=1.0)
    logging.basicConfig(level=logging.INFO)

    engine = create_async_engine(Config.DATABASE_URL, pool_size=100, max_overflow=20, pool_timeout=60)

    di_builder = setup_di_builder(engine)

    app = FastAPI(lifespan=partial(lifespan, di_builder))
    setup_routers(app)
    setup_exceptions(app)
    setup_middlewares(app)

    return app
