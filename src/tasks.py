import os
from datetime import datetime

from celery import Celery

from src.kernel import main as kernel_main
from src.models import CalcStatus
from src.service import CalculationsService

app = Celery("tasks", broker=os.getenv("CELERY_BROKER"), backend=os.getenv("CELERY_BACKEND"))


@app.task
def run_kenrel_calc(calc_id: int):
    """
    Run kernel calculation for the saved item
    """
    service = CalculationsService()

    calculation = service.read_one(id=calc_id)
    service.update(id=calculation.id, status=CalcStatus.PROCESSING.value, calc_start=datetime.now())

    results = kernel_main(date_start=calculation.date_start, date_fin=calculation.date_fin, lag=calculation.lag)

    service.update(id=calculation.id, status=CalcStatus.COMPLETE.value, calc_fin=datetime.now())
    service.bulk_insert_results(calc_id, results.to_dict("records"))
