from rich.layout import Layout
from rich.panel import Panel

from kanban.db_models import Column
from kanban.task.changers import get_by_column_id

INPUT_FIELDS_AND_VALIDATORS = {
    "code": "code",
    "title": "required|str",
    "is_important": "bool",
    "description": "str",
    "deadline": "datetime",
}


def get_task_layouts(columns: list[Column]) -> dict[str, list[Layout]]:
    cards_by_columns = {}
    for column in columns:
        cards = []
        tasks = get_by_column_id(column.id)
        for task in tasks:
            if task is None:
                continue
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
