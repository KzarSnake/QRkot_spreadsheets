from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

from app.core.constants import LENGTH, MIN_LENGTH


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=MIN_LENGTH, max_length=LENGTH)
    description: str = Field(..., min_length=MIN_LENGTH)
    full_amount: PositiveInt

    class Config:
        extra = 'forbid'


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(min_length=MIN_LENGTH, max_length=LENGTH)
    description: Optional[str] = Field(min_length=MIN_LENGTH)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = 'forbid'


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
