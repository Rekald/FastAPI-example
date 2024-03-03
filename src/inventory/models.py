from fastapi import Query
from pydantic import BaseModel
from typing import Optional, Annotated


class InventoryRow(BaseModel):
    id: Optional[int] = None
    part_code: str
    description: str
    producer: str
    quantity: Annotated[int, Query(ge=1)]
    catalog_price: Annotated[float, Query(ge=0)]
    discount: Annotated[float, Query(ge=0)]
    buy_price: Annotated[float, Query(ge=0)]
    total_value: Annotated[float, Query(ge=0)]
