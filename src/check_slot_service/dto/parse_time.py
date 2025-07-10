from datetime import datetime, time, date

from pydantic import BaseModel, field_validator


class ParseTime(BaseModel):
    start_time: str | time
    end_time: str | time

    @field_validator("start_time", "end_time", mode="before")
    def validate_time(cls, value):
        try:
            return (
                value
                if isinstance(value, time)
                else datetime.strptime(value, "%H:%M").time()
            )
        except ValueError:
            raise ValueError(f"Неверный формат времени: {value}. Ожидается HH:MM")


class ParseDate(BaseModel):
    date: date


class ParseDateTime(ParseDate, ParseTime): ...
