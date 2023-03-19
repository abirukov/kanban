import datetime

import pytest

from db import DB_SESSION
from kanban.column.changers import fetch_from_db_by_code as column_fetch_by_code
from kanban.task.changers import fetch_from_db_by_code as task_fetch_by_code
from kanban.db_models import Column, Task
from main import create, create_column, update, update_column, delete_column, delete, move

COLUMN_VALID_USER_INPUT_VALUES = {
    "code": "start",
    "title": "start",
    "color": "red",
    "sort": 100,
}

TASK_VALID_USER_INPUT_VALUES = {
    "title": "test_task",
    "code": "test_task",
    "is_important": False,
    "description": "test_task",
    "deadline": datetime.datetime.now(),
}

NOT_CREATED_CODE = "not_created"


def test__show():
    pass


def test__create__success(start_column_saved, main_get_input_values_mock):
    main_get_input_values_mock.return_value = TASK_VALID_USER_INPUT_VALUES

    create()
    task = task_fetch_by_code(TASK_VALID_USER_INPUT_VALUES["code"])

    assert task is not None

    Task.query.filter_by(id=task.id).delete()
    DB_SESSION.commit()


def test__create__fail(test_task, main_get_input_values_mock):
    with pytest.raises(RuntimeError, match=r"Колонки не найдены, создайте хотя бы одну"):
        main_get_input_values_mock.return_value = TASK_VALID_USER_INPUT_VALUES

        create()


def test__update__success(test_task_saved, start_column_saved, main_print_mock, main_get_input_values_mock):
    main_get_input_values_mock.return_value = TASK_VALID_USER_INPUT_VALUES
    TASK_VALID_USER_INPUT_VALUES["title"] = "test_task"

    update(test_task_saved.id)

    test_task_saved.title = "test_task"
    task_in_db = task_fetch_by_code(TASK_VALID_USER_INPUT_VALUES["code"])
    assert main_print_mock.mock_calls[0].args[0] == "Сделать вывод карточки"
    assert task_in_db == test_task_saved
    assert main_print_mock.mock_calls[-1].args[0] == "Задача изменена"


def test__update__fail(main_print_mock, main_get_input_values_mock):
    main_get_input_values_mock.return_value = TASK_VALID_USER_INPUT_VALUES

    update(NOT_CREATED_CODE)

    task_in_db = task_fetch_by_code(NOT_CREATED_CODE)
    assert main_print_mock.mock_calls[0].args[0] == "Сделать вывод карточки"
    assert task_in_db is None
    assert main_print_mock.mock_calls[-1].args[0] == "Задача не найдена"


def test__delete__success(test_task_saved, main_print_mock):

    delete(test_task_saved.code)

    task_in_db = task_fetch_by_code(test_task_saved.code)
    test_task_saved.is_delete = True
    assert task_in_db == test_task_saved
    assert main_print_mock.mock_calls[-1].args[0] == "Задача удалена"


def test__delete__fail(main_print_mock):

    delete(NOT_CREATED_CODE)

    task_in_db = task_fetch_by_code(NOT_CREATED_CODE)
    assert task_in_db is None
    assert main_print_mock.mock_calls[-1].args[0] == "Задача не найдена"


def test__move__success(test_task_saved, start_column_saved, main_print_mock):

    move(test_task_saved.code, start_column_saved.code)

    test_task_saved.column_id = start_column_saved.id
    task_in_db = task_fetch_by_code(test_task_saved.code)
    assert task_in_db == test_task_saved
    assert main_print_mock.mock_calls[-1].args[0] == "Задача перемещена"


def test__move__fail_by_column(test_task_saved, main_print_mock):

    move(test_task_saved.code, NOT_CREATED_CODE)

    assert main_print_mock.mock_calls[-1].args[0] == "Колонка не найдена"


def test__move__fail_by_task(main_print_mock):
    move(NOT_CREATED_CODE, NOT_CREATED_CODE)

    assert main_print_mock.mock_calls[-1].args[0] == "Задача не найдена"


def test__create_column__success(main_get_input_values_mock):
    main_get_input_values_mock.return_value = COLUMN_VALID_USER_INPUT_VALUES

    create_column()

    column = column_fetch_by_code(COLUMN_VALID_USER_INPUT_VALUES["code"])
    assert column is not None

    Column.query.filter_by(id=column.id).delete()
    DB_SESSION.commit()


def test__update_column__success(start_column_saved, main_print_mock, main_get_input_values_mock) -> None:
    COLUMN_VALID_USER_INPUT_VALUES["color"] = "pink"
    main_get_input_values_mock.return_value = COLUMN_VALID_USER_INPUT_VALUES

    update_column(start_column_saved.code)

    column_in_db = column_fetch_by_code(COLUMN_VALID_USER_INPUT_VALUES["code"])
    start_column_saved.color = "pink"
    assert main_print_mock.mock_calls[0].args[0] == "Сделать вывод карточки"
    assert column_in_db == start_column_saved
    assert main_print_mock.mock_calls[-1].args[0] == "Колонка изменена"


def test__update_column__fail(main_print_mock, main_get_input_values_mock) -> None:
    main_get_input_values_mock.return_value = COLUMN_VALID_USER_INPUT_VALUES

    update_column(NOT_CREATED_CODE)

    column_in_db = column_fetch_by_code(NOT_CREATED_CODE)
    assert main_print_mock.mock_calls[0].args[0] == "Сделать вывод карточки"
    assert column_in_db is None
    assert main_print_mock.mock_calls[-1].args[0] == "Колонка не найдена"


def test__delete_column__success(start_column_saved, main_print_mock):

    delete_column(start_column_saved.code)

    column_in_db = column_fetch_by_code(start_column_saved.code)
    start_column_saved.is_delete = True
    assert column_in_db == start_column_saved
    assert main_print_mock.mock_calls[-1].args[0] == "Колонка удалена"


def test__delete_column__fail(main_print_mock):

    delete_column(NOT_CREATED_CODE)

    column_in_db = column_fetch_by_code(NOT_CREATED_CODE)
    assert column_in_db is None
    assert main_print_mock.mock_calls[-1].args[0] == "Колонка не найдена"
