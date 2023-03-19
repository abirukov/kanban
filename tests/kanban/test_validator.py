from kanban.enums import InputEntities
from kanban.validator import Validator


def test__validate__success():
    result = Validator(
        value="string",
        validate_types="str",
        input_entity_type=InputEntities.TASK,
    ).validate()
    assert result is True


def test__validate__fail():
    result = Validator(
        value="s",
        validate_types="bool",
        input_entity_type=InputEntities.TASK,
    ).validate()
    assert result is False


def test__validate_str__success():
    result = Validator(
        value="string",
        validate_types="str",
        input_entity_type=InputEntities.TASK,
    ).validate_str()
    assert result is True


def test__validate_str__fail():
    result = Validator(
        value=123,
        validate_types="str",
        input_entity_type=InputEntities.TASK,
    ).validate_str()
    assert result is False


def test__validate_int__success():
    result = Validator(
        value="123",
        validate_types="int",
        input_entity_type=InputEntities.TASK,
    ).validate_int()
    assert result is True


def test__validate_int__fail():
    result = Validator(
        value="string",
        validate_types="int",
        input_entity_type=InputEntities.TASK,
    ).validate_int()
    assert result is False


def test__validate_color__success():
    result = Validator(
        value="red",
        validate_types="color",
        input_entity_type=InputEntities.TASK,
    ).validate_color()
    assert result is True


def test__validate_color__fail():
    result = Validator(
        value="unknown",
        validate_types="color",
        input_entity_type=InputEntities.TASK,
    ).validate_color()
    assert result is False


def test__validate_bool__success():
    result = Validator(
        value="Y",
        validate_types="bool",
        input_entity_type=InputEntities.TASK,
    ).validate_bool()
    assert result is True


def test__validate_bool__fail():
    result = Validator(
        value="no",
        validate_types="bool",
        input_entity_type=InputEntities.TASK,
    ).validate_bool()
    assert result is False


def test__validate_required__success():
    result = Validator(
        value="required",
        validate_types="required",
        input_entity_type=InputEntities.TASK,
    ).validate_required()
    assert result is True


def test__validate_required__fail():
    result = Validator(
        value="",
        validate_types="required",
        input_entity_type=InputEntities.TASK,
    ).validate_required()
    assert result is False


def test__validate_code__task_success():
    result = Validator(
        value="code",
        validate_types="code",
        input_entity_type=InputEntities.TASK,
    ).validate_code()
    assert result is True


def test__validate_code__task_fail(test_task_saved):
    result = Validator(
        value=test_task_saved.code,
        validate_types="code",
        input_entity_type=InputEntities.TASK,
    ).validate_code()
    assert result is False


def test__validate_code__column_success():
    result = Validator(
        value="code",
        validate_types="code",
        input_entity_type=InputEntities.COLUMN,
    ).validate_code()
    assert result is True


def test__validate_code__column_fail(start_column_saved):
    result = Validator(
        value=start_column_saved.code,
        validate_types="code",
        input_entity_type=InputEntities.COLUMN,
    ).validate_code()
    assert result is False


def test__validate_datetime__success():
    result = Validator(
        value="20:00",
        validate_types="datetime",
        input_entity_type=InputEntities.TASK,
    ).validate_datetime()
    assert result is True


def test__validate_datetime__fail():
    result = Validator(
        value="someday",
        validate_types="datetime",
        input_entity_type=InputEntities.TASK,
    ).validate_datetime()
    assert result is False
