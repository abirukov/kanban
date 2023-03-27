from db import DB_SESSION
from kanban.db_models import Column, Task, Entities


def save_to_db(db_model: Column | Task) -> Column | Task:
    DB_SESSION.add(db_model)
    DB_SESSION.commit()
    return db_model


def update_in_db(type: Entities, id: int, new_fields: dict) -> None:
    DB_SESSION.query(type.value).filter(
        type.value.id == id,
    ).update(
        new_fields, synchronize_session=False,
    )
    DB_SESSION.commit()


def fetch_from_db_by_id(type: Entities, id: int) -> Column | Task | None:
    return type.value.query.filter(type.value.id == id).first()


def fetch_from_db_by_code(type: Entities, code: str) -> Column | Task | None:
    return type.value.query.filter(type.value.code == code).first()


def get_undeleted_by_sort(type: Entities) -> list[Column | Task | None]:
    return type.value.query.filter(
        type.value.is_delete.is_(False),
    ).order_by(
        type.value.sort.asc(),
    ).all()


def fetch_from_db(type: Entities, code_or_id: str) -> Column | Task | None:
    try:
        int_code_or_id = int(code_or_id)
        by_id_result = fetch_from_db_by_id(type, int_code_or_id)
    except ValueError:
        by_id_result = None
    if by_id_result is not None:
        return by_id_result
    return fetch_from_db_by_code(type, code_or_id)
