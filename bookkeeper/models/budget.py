"""
Описан класс, представляющий описание бюджета
"""

from dataclasses import dataclass, field
from datetime import datetime

from bookkeeper.repository.abstract_repository import AbstractRepository

@dataclass(slots=True)
class Budget:
    """
    Бюджет (совокупность расходов за период времени).
    name - название периода
    begin_period_date - дата начала отсчета
    end_period_date - дата конца отсчета
    value - сумма расходов за данный период
    comment - комментарий
    pk - id записи в базе данных
    """

    name: str = 'Период'
    begin_period_date: datetime = field(default_factory=datetime.now)
    end_period_date: datetime = field(default_factory=datetime.now)
    value: float = 0
    comment: str = ''
    pk: int = 0
    _: AbstractRepository = None

