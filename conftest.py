import datetime
from unittest.mock import patch

import pytest
import typer

from db import DB_SESSION
from kanban.db_models import Column, Task
from kanban.db_utils import save_to_db


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
    save_to_db(start_column)
    yield start_column
    Column.query.filter_by(id=start_column.id).delete()
    DB_SESSION.commit()


@pytest.fixture
def finish_column_saved(finish_column):
    save_to_db(finish_column)
    yield finish_column
    Column.query.filter_by(id=finish_column.id).delete()
    DB_SESSION.commit()


@pytest.fixture
def deleted_column_saved(deleted_column):
    save_to_db(deleted_column)
    yield deleted_column
    Column.query.filter_by(id=deleted_column.id).delete()
    DB_SESSION.commit()


@pytest.fixture
def main_print_mock():
    with patch("main.print") as print_mock:
        yield print_mock


@pytest.fixture
def utils_ask_questions_mock():
    with patch("main.ask_questions") as utils_ask_questions_mock:
        yield utils_ask_questions_mock


@pytest.fixture
def test_task():
    return Task(title="test_task", code="test_task", is_important=False, description="test_task",
                created_at=datetime.datetime.now(), updated_at=datetime.datetime.now(),
                deadline=datetime.datetime.now() + datetime.timedelta(days=1), is_delete=False)


@pytest.fixture
def test_task_saved(test_task, start_column_saved):
    test_task.column_id = start_column_saved.id
    save_to_db(test_task)
    yield test_task
    Task.query.filter_by(id=test_task.id).delete()
    DB_SESSION.commit()
