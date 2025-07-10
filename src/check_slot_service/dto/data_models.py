from pydantic import BaseModel


class DayModel(BaseModel):
    id: int
    date: str
    start: str
    end: str


class TimeslotModel(BaseModel):
    id: int
    day_id: int
    start: str
    end: str
