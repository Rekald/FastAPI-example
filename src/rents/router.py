from typing import Annotated
from fastapi import APIRouter, Request, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse

from src.rents.models import RentRow
from src.dependencies import templates
from src.rents import services as rent_services


rents_router = APIRouter()


@rents_router.put("/row")
async def generate(row: RentRow):
    rent_services.update_row(row)
    return HTMLResponse(status_code=200)


@rents_router.delete("/row")
async def generate(row_id: Annotated[int, Query(ge=0)]):
    rent_services.del_row(row_id)
    return HTMLResponse(status_code=200)


@rents_router.post("/row")
async def generate(row: RentRow):
    rent_services.add_row(row)
    return HTMLResponse(status_code=200)

#   -----------------------------------


@rents_router.get('/')
async def index(request: Request):
    return templates.TemplateResponse("rents/rents.html", {'request': request})


@rents_router.get('/datatable')
async def index(draw: Annotated[int, Query(ge=0)], start: Annotated[int, Query(ge=0)], length: Annotated[int, Query(ge=0)], search: str = Query(default=None, alias="search[value]")):
    rows: dict = rent_services.get_filtered_rents(draw, start, length, search)
    return JSONResponse(jsonable_encoder(rows))
