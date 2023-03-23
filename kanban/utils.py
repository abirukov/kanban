import datetime
from typing import Any

from dateutil import parser
from rich.layout import Layout
from rich.panel import Panel

from kanban.changers import Changer
from kanban.db_models import Column, Task
from kanban.enums import Entities
from kanban.validator import Validator, BOOLEAN_SYMBOLS


def ask_questions(dict_params: dict[str, Any], input_entity_type: Entities) -> dict:
    prepared_params = {}
    for param in dict_params:
        prepared_params[param] = ask_one_question(param, dict_params[param], input_entity_type)
    return prepared_params


def ask_one_question(param: str, param_type: str, input_entity_type: Entities) -> str | bool | datetime:
    is_valid = False
    while not is_valid:
        raw_input = input(f"Please input {param}: ")
        is_valid = Validator(
            value=raw_input.strip(),
            validate_types=param_type,
            input_entity_type=input_entity_type,
        ).validate()
        if is_valid:
            return modify_answer(raw_input, param_type)


def modify_answer(raw_input: str, param_type: str) -> str | bool | datetime:
    if "bool" in param_type:
        answer = BOOLEAN_SYMBOLS[raw_input]
    elif "datetime" in param_type:
        answer = parser.parse(raw_input)
    else:
        answer = raw_input
    return answer


def fetch_from_db(code_or_id: str, db_type: Entities) -> Column | Task | None:
    changer = Changer(db_type)
    try:
        int_code_or_id = int(code_or_id)
        by_id_result = changer.fetch_from_db_by_id(int_code_or_id)
    except ValueError:
        by_id_result = None
    if by_id_result is not None:
        return by_id_result
    return changer.fetch_from_db_by_code(code_or_id)


def get_task_layouts(columns: list[Column]) -> dict[str, list[Layout]]:
    cards_by_columns = {}
    for column in columns:
        cards = []
        tasks = get_tasks_by_column_id(column.id)
        for task in tasks:
            task_layout = Layout(Panel(
                f"[bold]{task.title}[/bold]\n"
                f"code: {task.code}\n"
                f"is_important: {task.is_important}\n"
                f"description: {task.description}\n"
                f"created_at: {task.created_at}\n"
                f"updated_at: {task.updated_at}\n"
                f"deadline: {task.deadline}",
                style=column.color,
            ))
            cards.append(task_layout)
        cards_by_columns[column.code] = cards
    return cards_by_columns


def get_tasks_by_column_id(column_id: int) -> list[Task | None]:
    return Task.query.filter(Task.column_id == column_id).all()
