from unittest.mock import patch

from dateutil import parser

from kanban.enums import InputEntities
from kanban.task.utils import INPUT_FIELDS_AND_VALIDATORS
from kanban.utils import get_user_input_values


def test_get_user_input_values():
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
        "deadline": parser.parse("19-03-2023"),
    }
    with patch("kanban.utils.input") as mock_input:
        mock_input.side_effect = input_values
        values = get_user_input_values(INPUT_FIELDS_AND_VALIDATORS, InputEntities.TASK)
        assert expected_values == values
