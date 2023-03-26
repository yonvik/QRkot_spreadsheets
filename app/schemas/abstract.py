from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TimeAndCashModel(BaseModel):
    """Абстрактная модель для пожертвований и проектов."""

    invested_amount: int = Field(ge=0)
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]
