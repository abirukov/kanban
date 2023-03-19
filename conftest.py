import datetime
from unittest.mock import patch

import pytest
import typer

from db import DB_SESSION
from kanban.db_models import Column, Task
from kanban.column.changers import save_to_db as column_save
from kanban.task.changers import save_to_db as task_save


@pytest.fixture
def app():
    return typer.Typer()


@pytest.fixture
def start_column():
    return Column(code="start", title="start", color="red", sort=100, is_delete=False)


@pytest.fixture
def finish_column():
    return Column(code="finish", title="finish", color="green", sort=200, is_delete=False)


@pytest.fixture
def deleted_column():
    return Column(code="deleted", title="deleted", color="blue", sort=300, is_delete=True)


@pytest.fixture
def start_column_saved(start_column):
    column_save(start_column)
    yield start_column
    Column.query.filter_by(id=start_column.id).delete()
    DB_SESSION.commit()


@pytest.fixture
def finish_column_saved(finish_column):
    column_save(finish_column)
    yield finish_column
    Column.query.filter_by(id=finish_column.id).delete()
    DB_SESSION.commit()


@pytest.fixture
def deleted_column_saved(deleted_column):
    column_save(deleted_column)
    yield deleted_column
    Column.query.filter_by(id=deleted_column.id).delete()
    DB_SESSION.commit()


@pytest.fixture
def main_print_mock():
    with (patch("main.print") as print_mock):
        yield print_mock


@pytest.fixture
def main_get_input_values_mock():
    with (patch("main.get_user_input_values") as main_get_user_input_values_mock):
        yield main_get_user_input_values_mock


@pytest.fixture
def test_task():
    return Task(title="test_task", code="test_task", is_important=False, description="test_task",
                created_at=datetime.datetime.now(), updated_at=datetime.datetime.now(),
                deadline=datetime.datetime.now() + datetime.timedelta(days=1), is_delete=False)


@pytest.fixture
def test_task_saved(test_task, start_column_saved):
    test_task.column_id = start_column_saved.id
    task_save(test_task)
    yield test_task
    Task.query.filter_by(id=test_task.id).delete()
    DB_SESSION.commit()
