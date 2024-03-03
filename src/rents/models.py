from fastapi import Query
from pydantic import BaseModel
from typing import Optional, Annotated


class RentRow(BaseModel):
    id: Optional[int] = None
    part_code: str
    description: str
    quantity: Annotated[int, Query(ge=1)]
    position: str
    rent_date: str
    rent_expiration: Optional[str] = None
