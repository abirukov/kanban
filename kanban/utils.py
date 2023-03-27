from datetime import datetime
from typing import Any

from dateutil import parser
from rich.layout import Layout
from rich.panel import Panel

from kanban.db_models import Column, Task, Entities
from kanban.validator import BOOLEAN_SYMBOLS, validate


def ask_questions(dict_params: dict[str, Any], input_entity_type: Entities) -> dict:
    prepared_params = {}
    for param in dict_params:
        prepared_params[param] = ask_one_question(param, dict_params[param], input_entity_type)
    return prepared_params


def ask_one_question(param: str, param_type: str, input_entity_type: Entities) -> str | bool | datetime:
    is_valid = False
    while not is_valid:
        raw_input = input(f"Please input {param}: ")
        is_valid = validate(
            value=raw_input.strip(),
            validate_types=param_type,
            input_entity_type=input_entity_type,
        )
        if is_valid:
            return modify_answer(raw_input, param_type)
    return False


def modify_answer(raw_input: str, param_type: str) -> str | bool | datetime:
    if "bool" in param_type:
        return BOOLEAN_SYMBOLS[raw_input]
    elif "datetime" in param_type:
        return parser.parse(raw_input)
    else:
        return raw_input


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


def get_tasks_by_column_id(column_id: int) -> list[Task]:
    return Task.query.filter(Task.column_id == column_id).all()
