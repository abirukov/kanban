from unittest.mock import patch

import pytest
from dateutil import parser

from kanban.constants import TASK_INPUT_FIELDS_AND_VALIDATORS
from kanban.db_models import Entities
from kanban.utils import ask_questions, modify_answer, ask_one_question, get_task_layouts, \
    get_tasks_by_column_id


def test_ask_questions():
    input_values = [
        "test_task",
        "test_task",
        "n",
        "test_task",
        "19-03-2023",
    ]

    expected_values = {
        "code": "test_task",
        "title": "test_task",
        "is_important": False,
        "description": "test_task",
        "deadline": parser.parse("19.03.2023"),
    }
    with patch("kanban.utils.input") as mock_input:
        mock_input.side_effect = input_values
        values = ask_questions(TASK_INPUT_FIELDS_AND_VALIDATORS, Entities.TASK)
        assert expected_values == values


@pytest.mark.parametrize(
    "param, raw_input, param_type, expected",
    [
        ("description", "test", "str", "test"),
        ("deadline", "19.03.2023", "datetime", parser.parse("19.03.2023")),
        ("is_important", "Y", "bool", True),
    ],
)
def test_ask_one_question(param, raw_input, param_type, expected):
    with patch("kanban.utils.input") as mock_input:
        mock_input.return_value = raw_input
        assert ask_one_question(param, param_type, Entities.TASK) == expected


@pytest.mark.parametrize(
    "raw_input, param_type, expected",
    [
        ("test", "str", "test"),
        ("19.03.2023", "datetime", parser.parse("19.03.2023")),
        ("Y", "bool", True),
    ],
)
def test_modify_answer(raw_input, param_type, expected):
    assert modify_answer(raw_input, param_type) == expected


def test_get_task_layouts(test_task_saved, start_column):
    cards_by_columns = get_task_layouts([start_column])

    assert len(cards_by_columns[start_column.code]) == 1


def test_get_tasks_by_column_id(test_task_saved, start_column):
    assert get_tasks_by_column_id(start_column.id)
