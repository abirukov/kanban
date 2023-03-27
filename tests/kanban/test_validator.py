import pytest

from kanban.db_models import Entities
from kanban.validator import validate, validate_str, validate_int, validate_color, validate_bool, validate_required, \
    validate_code, validate_datetime


def test__validate__success():
    result = validate(
        value="string",
        validate_types="str",
        input_entity_type=Entities.TASK,
    )
    assert result is True


def test__validate__fail():
    result = validate(
        value="s",
        validate_types="bool",
        input_entity_type=Entities.TASK,
    )
    assert result is False


def test__validate_str__success():
    assert validate_str("string") is True


def test__validate_str__fail():
    assert validate_str(123) is False


def test__validate_int__success():
    assert validate_int("123") is True


def test__validate_int__fail():
    assert validate_int("string") is False


def test__validate_color__success():
    assert validate_color("red") is True


def test__validate_color__fail():
    assert validate_color("unknown") is False


def test__validate_bool__success():
    assert validate_bool("Y") is True


def test__validate_bool__fail():
    assert validate_bool("no") is False


def test__validate_required__success():
    assert validate_required("required") is True


def test__validate_required__fail():
    assert validate_required("") is False


@pytest.mark.parametrize(
    "entity_type",
    [
        Entities.COLUMN,
        Entities.TASK,
    ],
)
def test__validate_code__task_success(entity_type):
    assert validate_code("code", entity_type) is True


@pytest.mark.parametrize(
    "entity_type, saved_model",
    [
        (Entities.COLUMN, pytest.lazy_fixture("start_column_saved")),
        (Entities.TASK, pytest.lazy_fixture("test_task_saved")),
    ],
)
def test__validate_code__task_fail(entity_type, saved_model):
    assert validate_code(saved_model.code, entity_type) is False


def test__validate_datetime__success():
    assert validate_datetime("20:00") is True


def test__validate_datetime__fail():
    assert validate_datetime("someday") is False
