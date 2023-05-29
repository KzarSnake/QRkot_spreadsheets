from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

MAX_LIMIT = 100
MIN_LIMIT = 1

class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=MIN_LIMIT, max_length=MAX_LIMIT)
    description: str = Field(..., min_length=MIN_LIMIT)
    full_amount: PositiveInt

    class Config:
        extra = 'forbid'


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(min_length=MIN_LIMIT, max_length=MAX_LIMIT)
    description: Optional[str] = Field(min_length=MIN_LIMIT)
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
