from pydantic import BaseModel, Field

class MatchingModel(BaseModel):
    id_jd: str = Field(...)
    id_cv: str = Field(...)
    config_score: dict = Field(...)