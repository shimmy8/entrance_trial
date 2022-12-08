from datetime import date
from typing import Literal

from fastapi import Body, Depends, FastAPI, Query

from src.schemas import CalculationCreate, CalculationGet, CalculationsList
from src.service import CalculationsService
from src.tasks import run_kenrel_calc

app = FastAPI()


@app.get("/calculations", response_model=list[CalculationsList])
async def calculations_list(
    service: CalculationsService = Depends(CalculationsService),
    order: Literal["asc", "desc"] = "asc",
    limit: int = 10,
    offset: int = 0,
):
    """
    Get list of a calculations
    """
    items = service.read_many(order=order, limit=limit, offset=offset)
    return items


@app.get("/calculations/{calc_id}", response_model=CalculationGet, response_model_exclude_unset=True)
async def read_calculation(
    calc_id: int,
    fields: list[Literal["calc_start", "calc_fin", "calc_time", "date_start", "date_fin", "lag"]]
    | None = Query(default=None),
    service: CalculationsService = Depends(CalculationsService),
):
    """
    Read one specific calculation
    """
    item = service.read_one(id=calc_id, with_results=True)
    if fields:
        return service.strip_task_fields(item, fields)
    return item


@app.post("/calculations", response_model=CalculationCreate)
def create_calculation(
    service: CalculationsService = Depends(CalculationsService),
    date_start: date = Body(),
    date_fin: date = Body(),
    lag: int = Body(),
):
    """
    Create new calculation
    """
    new_obj = service.create(date_start=date_start, date_fin=date_fin, lag=lag)
    run_kenrel_calc.delay(calc_id=new_obj.id)
    return new_obj
