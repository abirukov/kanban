from db import DB_SESSION
from kanban.column.changers import save_to_db, update_in_db, fetch_from_db_by_id, fetch_from_db_by_code, \
    fetch_from_db, get_undeleted_by_sort
from kanban.db_models import Column


def test__save_to_db(start_column):
    save_to_db(start_column)

    column_in_db = fetch_from_db(start_column.code)
    assert start_column == column_in_db
    Column.query.filter_by(id=column_in_db.id).delete()
    DB_SESSION.commit()


def test__update_in_db(start_column_saved):
    update_in_db(start_column_saved.id, {"title": "start_column_updated"})

    column_in_db = fetch_from_db(start_column_saved.code)
    start_column_saved.title = "start_column_updated"
    assert start_column_saved == column_in_db


def test__fetch_from_db_by_id(start_column_saved):
    column_in_db = fetch_from_db_by_id(start_column_saved.id)
    assert start_column_saved == column_in_db


def test__fetch_from_db_by_code(start_column_saved):
    column_in_db = fetch_from_db_by_code(start_column_saved.code)
    assert start_column_saved == column_in_db


def test__fetch_from_db__code(start_column_saved):
    column_in_db = fetch_from_db(start_column_saved.code)
    assert start_column_saved == column_in_db


def test__fetch_from_db__id(start_column_saved):
    column_in_db = fetch_from_db(start_column_saved.id)
    assert start_column_saved == column_in_db


def test__get_undeleted_by_sort(start_column_saved, finish_column_saved):
    columns_list = get_undeleted_by_sort()
    assert columns_list == [start_column_saved, finish_column_saved]
