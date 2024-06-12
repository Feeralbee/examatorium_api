from pydantic import BaseModel


class QuestionsCount(BaseModel):
    all: int
    task_questions: int

    class Config:
        from_attributes = True
        orm_mode = True
