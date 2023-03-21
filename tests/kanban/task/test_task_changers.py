from db import DB_SESSION
from kanban.task.changers import save_to_db, update_in_db, fetch_from_db_by_id, fetch_from_db_by_code, \
    fetch_from_db
from kanban.db_models import Task


def test__save_to_db(test_task_saved):
    save_to_db(test_task_saved)

    task_in_db = fetch_from_db(test_task_saved.code)
    assert test_task_saved == task_in_db
    Task.query.filter_by(id=task_in_db.id).delete()
    DB_SESSION.commit()


def test__update_in_db(test_task_saved):
    update_in_db(test_task_saved.id, {"title": "test_task_updated"})

    task_in_db = fetch_from_db(test_task_saved.code)
    test_task_saved.title = "test_task_updated"
    assert test_task_saved == task_in_db


def test__fetch_from_db_by_id(test_task_saved):
    task_in_db = fetch_from_db_by_id(test_task_saved.id)
    assert test_task_saved == task_in_db


def test__fetch_from_db_by_code(test_task_saved):
    task_in_db = fetch_from_db_by_code(test_task_saved.code)
    assert test_task_saved == task_in_db


def test__fetch_from_db__code(test_task_saved):
    task_in_db = fetch_from_db(test_task_saved.code)
    assert test_task_saved == task_in_db


def test__fetch_from_db__id(test_task_saved):
    task_in_db = fetch_from_db(test_task_saved.id)
    assert test_task_saved == task_in_db
