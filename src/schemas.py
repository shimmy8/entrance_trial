from datetime import date, datetime

from pydantic import BaseModel


class CalculationCreate(BaseModel):
    id: int
    status: str
    date_start: date
    date_fin: date
    lag: int

    class Config:
        orm_mode = True


class CalculationsList(BaseModel):
    id: int
    status: str
    calc_start: datetime | None

    class Config:
        orm_mode = True


class CalculationResult(BaseModel):
    date: date
    liquid: float
    oil: float
    water: float
    wct: float

    class Config:
        orm_mode = True


class CalculationGet(BaseModel):
    id: int
    status: str
    calc_start: datetime | None
    calc_fin: datetime | None
    calc_time: int | None
    date_start: date | None
    date_fin: date | None
    lag: int | None
    results: list[CalculationResult]

    class Config:
        orm_mode = True
