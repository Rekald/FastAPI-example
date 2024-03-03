from sqlalchemy import desc, asc
from sqlalchemy.exc import OperationalError
from types import FunctionType
from src.database import Session, Inventory
from src.inventory.models import InventoryRow
from src.inventory.utils import get_dataframe_from_inventory, gen_xls_report

col_ord_map = {"4": Inventory.quantity, "8": Inventory.total_value}
col_dir_map = {"asc": asc, "desc": desc}


def update_row(row: InventoryRow):
    try:
        with Session.begin() as session:
            row_to_update: Inventory = session.query(Inventory).get(row.id)
            row_to_update.part_code = row.part_code
            row_to_update.description = row.description
            row_to_update.producer = row.producer
            row_to_update.quantity = row.quantity
            row_to_update.catalog_price = row.catalog_price
            row_to_update.discount = row.discount
            row_to_update.buy_price = row.buy_price
            row_to_update.total_value = row.total_value
        return True
    except OperationalError:
        return False


def del_row(row_id: int):
    try:
        with Session.begin() as session:
            row_to_delete = session.query(Inventory).get(row_id)
            session.delete(row_to_delete)
        return True
    except OperationalError:
        return False


def add_row(row: InventoryRow):
    try:
        with Session.begin() as session:
            new_row = Inventory(part_code=row.part_code, description=row.description, producer=row.producer,
                                quantity=row.quantity, catalog_price=row.catalog_price, discount=row.discount,
                                buy_price=row.buy_price, total_value=row.total_value)
            session.add(new_row)
        return True
    except OperationalError:
        return False


def get_filtered_inventory(draw, start: int, length: int, search: str, col_ord: str, col_dir: str) -> dict:
    rows: list[InventoryRow] = get_inventory(col_ord_map.get(col_ord, Inventory.quantity),
                                             col_dir_map.get(col_dir, desc))
    records_total = len(rows)
    if search:
        search = search.lower()
        rows = [row for row in rows if
                search in row.part_code.lower() or
                search in row.description.lower() or
                search in row.producer.lower() or
                search in str(row.catalog_price) or
                search in str(row.total_value)]
    records_filtered = len(rows)

    min(start + length, records_filtered)
    rows = rows[start: start + length]

    response_data = {
        "data": rows,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered
    }

    return response_data


def get_inventory(col_to_ord=None, ord_func: FunctionType = None) -> list[InventoryRow]:
    with Session.begin() as session:
        if col_to_ord is not None and ord_func is not None:
            rows: list[Inventory] = session.query(Inventory).order_by(ord_func(col_to_ord)).all()
        else:
            rows: list[Inventory] = session.query(Inventory).all()
        inventory_rows: list[InventoryRow] = [
            InventoryRow(id=row.id, part_code=row.part_code, description=row.description,
                         producer=row.producer, quantity=row.quantity,
                         catalog_price=row.catalog_price,
                         discount=row.discount, buy_price=row.buy_price,
                         total_value=row.total_value) for row in rows]
    return inventory_rows


def get_row(row_id: int):
    with Session.begin() as session:
        row = session.query(Inventory).get(row_id)
        if not row:
            return None
        return InventoryRow(id=row.id, part_code=row.part_code, description=row.description,
                            producer=row.producer, quantity=row.quantity,
                            catalog_price=row.catalog_price,
                            discount=row.discount, buy_price=row.buy_price,
                            total_value=row.total_value)


def get_xls_report(inventory: list[InventoryRow]):
    df = get_dataframe_from_inventory(inventory)
    return gen_xls_report(df)


report_types = {"xls": get_xls_report}
