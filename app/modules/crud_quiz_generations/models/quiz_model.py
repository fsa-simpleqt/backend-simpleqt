from pydantic import BaseModel, Field

class GenQuizModel(BaseModel):
    id_jd: str = Field(...)
    json_quiz_gen: dict = Field(...)