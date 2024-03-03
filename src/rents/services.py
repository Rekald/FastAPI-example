from src.rents.models import RentRow
from src.database import Session, Rents


def update_row(row: RentRow):
    with Session.begin() as session:
        row_to_update: Rents = session.query(Rents).get(row.id)
        row_to_update.part_code = row.part_code
        row_to_update.description = row.description
        row_to_update.quantity = row.quantity
        row_to_update.position = row.position
        row_to_update.rent_date = row.rent_date


def del_row(row_id: int):
    with Session.begin() as session:
        row_to_delete = session.query(Rents).get(row_id)
        session.delete(row_to_delete)


def add_row(row: RentRow):
    with Session.begin() as session:
        new_row = Rents(id=row.id, part_code=row.part_code, description=row.description, quantity=row.quantity,
                        position=row.position, rent_date=row.rent_date)
        session.add(new_row)


def get_filtered_rents(draw, start, length, search: str) -> dict:
    rows: list[RentRow] = get_rents()
    records_total = len(rows)
    if search:
        search = search.lower()
        rows = [row for row in rows if
                search in row.part_code.lower() or
                search in row.description.lower()]
    records_filtered = len(rows)

    min(start + length, records_filtered)
    rows = rows[start: start + length]
    response_data = {
        "data": rows,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered
    }

    return response_data


def get_rents() -> list[RentRow]:
    with Session.begin() as session:
        rows: list[Rents] = session.query(Rents).all()
        rents_row: list[RentRow] = [RentRow(id=row.id, part_code=row.part_code, description=row.description,
                                            quantity=row.quantity, position=row.position, rent_date=row.rent_date,
                                            rent_expiration="0") for row in rows]
    return rents_row


def get_row(row_id: int):
    with Session.begin() as session:
        row = session.query(Rents).get(row_id)
        if not row:
            return None
        return RentRow(id=row.id, part_code=row.part_code, description=row.description,
                       quantity=row.quantity, position=row.position, rent_date=row.rent_date,
                       rent_expiration="0")
