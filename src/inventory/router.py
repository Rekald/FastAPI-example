from typing import Annotated
from fastapi import APIRouter, Request, Query
from starlette.background import BackgroundTask
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse

from src.inventory import services
from src.dependencies import templates
from src.inventory.models import InventoryRow
from src.inventory.utils import remove_file


inventory_router = APIRouter()


@inventory_router.put("/row")
async def generate(row: InventoryRow):
    services.update_row(row)
    return HTMLResponse(status_code=200)


@inventory_router.delete("/row")
async def generate(row_id: Annotated[int, Query(ge=0)]):
    services.del_row(row_id)
    return HTMLResponse(status_code=200)


@inventory_router.post("/row")
async def generate(row: InventoryRow):
    services.add_row(row)
    return HTMLResponse(status_code=200)

#   -----------------------------------


@inventory_router.get('/')
async def index(request: Request):
    return templates.TemplateResponse("inventory/inventory.html", {'request': request})


@inventory_router.get('/datatable')
async def index(draw: Annotated[int, Query(ge=0)], start: Annotated[int, Query(ge=0)], length: Annotated[int, Query(ge=0)], search: str = Query(default=None, alias="search[value]"),
                col_ord: str = Query(default="4", alias="order[0][column]",), col_dir: str = Query(default="desc", alias="order[0][dir]")):
    rows: dict = services.get_filtered_inventory(draw, start, length, search, col_ord, col_dir)
    return JSONResponse(jsonable_encoder(rows))


@inventory_router.get('/total')
async def index():
    rows: list[InventoryRow] = services.get_inventory()
    buy_total = round(sum(row.total_value for row in rows), 2)
    catalog_total = round(sum(row.catalog_price * row.quantity for row in rows), 2)
    marginality = catalog_total - buy_total
    return JSONResponse(jsonable_encoder({'buy_total': buy_total, 'catalog_total': catalog_total, 'marginality': marginality}))


@inventory_router.get('/report/{file_type}')
async def index(file_type: str):
    report_f = services.report_types.get(file_type, None)
    if report_f is None:
        return HTMLResponse(status_code=404)

    report_path = report_f(services.get_inventory())
    return FileResponse(report_path, filename="Inventory report.xls", background=BackgroundTask(remove_file, report_path))

