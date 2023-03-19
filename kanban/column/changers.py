from sqlalchemy import false

from db import DB_SESSION
from kanban.db_models import Column


def save_to_db(db_model: Column) -> Column:
    DB_SESSION.add(db_model)
    DB_SESSION.commit()
    return db_model


def update_in_db(id: int, new_fields: dict) -> None:
    DB_SESSION.query(Column).filter(
        Column.id == id,
    ).update(
        new_fields, synchronize_session=False,
    )
    DB_SESSION.commit()


def fetch_from_db_by_id(id: int) -> Column | None:
    return Column.query.filter(Column.id == id).first()


def fetch_from_db_by_code(code: str) -> Column | None:
    return Column.query.filter(Column.code == code).first()


def fetch_from_db(code_or_id: str) -> Column | None:
    try:
        by_id_result = fetch_from_db_by_id(int(code_or_id))
    except ValueError:
        by_id_result = None
    if by_id_result is not None:
        return by_id_result
    return fetch_from_db_by_code(code_or_id)


def get_undeleted_by_sort():
    return Column.query.filter(
        Column.is_delete == false(),
    ).order_by(
        Column.sort.asc(),
    ).all()
