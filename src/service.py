from sqlalchemy.orm import Session, selectinload

from src.db import DBSession
from src.models import CalculationResult, CalculationTask


class CalculationsService:
    """
    Class for
    """

    db_session: Session | None = None

    def __init__(self):
        self.db_session = DBSession()

    def __del__(self):
        self.db_session.close()

    def create(self, **kwargs):
        """
        Create new calculation task
        """
        new_obj = CalculationTask(**kwargs)
        self.db_session.add(new_obj)
        self.db_session.commit()
        self.db_session.refresh(new_obj)
        return new_obj

    def update(self, id: int, **kwargs):
        """
        Update calculation task
        """
        obj = self.read_one(id=id)
        for key, value in kwargs.items():
            setattr(obj, key, value)
        self.db_session.commit()

    def bulk_insert_results(self, task_id: int, results: list[dict] | None = None):
        """
        Bulk insert caclulation results to DB
        """
        objects = []
        if results is not None:
            for result in results:
                objects.append(CalculationResult(task_id=task_id, **result))
        self.db_session.bulk_save_objects(objects)
        self.db_session.commit()

    def _read(self, **kwargs):
        filters = []
        for column, value in kwargs.items():
            filters.append(getattr(CalculationTask, column) == value)
        return self.db_session.query(CalculationTask).filter(*filters)

    def read_one(self, id: int, with_results=False):
        if with_results:
            return self._read(id=id).options(selectinload(CalculationTask.results)).first()
        return self._read(id=id).first()

    def read_many(self, order: str = "asc", offset: int = 0, limit: int = 10, **kwargs):
        ordering = CalculationTask.calc_start.asc() if order == "asc" else CalculationTask.calc_start.desc()
        return self._read(**kwargs).order_by(ordering).limit(limit).offset(offset).all()

    @staticmethod
    def strip_task_fields(obj: CalculationTask, fields: list) -> dict:
        result_dict = {}
        display_fields = ["id", "status", "results"] + fields
        for field in display_fields:
            result_dict[field] = getattr(obj, field)
        return result_dict
