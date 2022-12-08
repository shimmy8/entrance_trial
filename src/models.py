import enum

from sqlalchemy import Column, Date, DateTime, Enum, Float, ForeignKey, Integer, orm
from sqlalchemy.ext.hybrid import hybrid_property

from src.db import Base


class CalcStatus(enum.Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETE = "complete"

    @classmethod
    def values(cls):
        return [c.value for c in cls]


class CalculationTask(Base):
    __tablename__ = "calculation_tasks"

    id = Column(Integer, primary_key=True)
    status = Column(Enum(*CalcStatus.values()), default=CalcStatus.QUEUED.value)
    calc_start = Column(DateTime)
    calc_fin = Column(DateTime)
    date_start = Column(Date)
    date_fin = Column(Date)
    lag = Column(Integer)

    results = orm.relationship("CalculationResult")

    @hybrid_property
    def calc_time(self):
        """
        Calculate execution time in seconds
        """
        if self.calc_fin and self.calc_start:
            return (self.calc_fin - self.calc_start).seconds


class CalculationResult(Base):
    __tablename__ = "calculation_results"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("calculation_tasks.id"))
    date = Column(Date)
    liquid = Column(Float)
    oil = Column(Float)
    water = Column(Float)
    wct = Column(Float)
