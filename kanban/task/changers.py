from db import DB_SESSION
from kanban.db_models import Task


def save_to_db(db_model: Task) -> Task:
    DB_SESSION.add(db_model)
    DB_SESSION.commit()
    return db_model


def update_in_db(id: int, new_fields: dict) -> None:
    DB_SESSION.query(Task).filter(
        Task.id == id,
    ).update(
        new_fields, synchronize_session=False,
    )
    DB_SESSION.commit()


def fetch_from_db_by_id(id: int) -> Task | None:
    return Task.query.filter(Task.id == id).first()


def fetch_from_db_by_code(code: str) -> Task | None:
    return Task.query.filter(Task.code == code).first()


def fetch_from_db(code_or_id: str) -> Task | None:
    try:
        by_id_result = fetch_from_db_by_id(int(code_or_id))
    except ValueError:
        by_id_result = None
    if by_id_result is not None:
        return by_id_result
    return fetch_from_db_by_code(code_or_id)
