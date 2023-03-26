from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.abstract import TimeAndCashModel


class DonationCreate(BaseModel):
    """Модель для создания пожертвования."""

    comment: Optional[str]
    full_amount: int = Field(..., gt=0)


class DonationtDB(DonationCreate):
    """Модель для получения информации о пожертвовании."""

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class ExtendedDonationtDB(DonationtDB, TimeAndCashModel):
    """Модель для получшения всей информации о пожертвовании."""

    user_id: int
