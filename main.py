import typer
from rich import print
from rich.layout import Layout
from rich.panel import Panel

from kanban.db_utils import get_undeleted_by_sort, save_to_db, update_in_db, fetch_from_db
from kanban.constants import COLUMN_INPUT_FIELDS_AND_VALIDATORS, TASK_INPUT_FIELDS_AND_VALIDATORS
from kanban.db_models import Column, Task, Entities
from kanban.utils import ask_questions, get_task_layouts

app = typer.Typer()


@app.command()
def show():
    layout = Layout()
    panels = []
    columns = get_undeleted_by_sort(Entities.COLUMN)
    task_layouts_by_column_code = get_task_layouts(columns)
    for column in columns:
        column_layout = Layout(
            Panel(
                f"[bold]{column.title}[/bold] code={column.code}",
                style=column.color,
            ),
            name=column.code,
        )
        panels.append(column_layout)
    layout.split(*panels, splitter="row")
    for column in columns:
        if task_layouts_by_column_code[column.code]:
            layout[column.code].split(*task_layouts_by_column_code[column.code])
    print(layout)


@app.command()
def create():
    columns = get_undeleted_by_sort(Entities.COLUMN)
    if len(columns) == 0:
        raise RuntimeError("Колонки не найдены, создайте хотя бы одну")
    task_values = ask_questions(TASK_INPUT_FIELDS_AND_VALIDATORS, Entities.TASK)
    task_values["column_id"] = columns[0].id
    save_to_db(Task(**task_values))


@app.command()
def update(code_or_id: str):
    print("Сделать вывод карточки")
    new_task_values = ask_questions(TASK_INPUT_FIELDS_AND_VALIDATORS, Entities.TASK)
    task = fetch_from_db(Entities.TASK, code_or_id)
    if task is None:
        print("Задача не найдена")
    else:
        update_in_db(Entities.TASK, task.id, new_task_values)
        print("Задача изменена")


@app.command()
def delete(code_or_id: str):
    task = fetch_from_db(Entities.TASK, code_or_id)
    if task is None:
        print("Задача не найдена")
    else:
        update_in_db(Entities.TASK, task.id, {"is_delete": True})
        print("Задача удалена")


@app.command()
def move(code_or_id: str, column_code_or_id: str):
    task = fetch_from_db(Entities.TASK, code_or_id)
    if task is None:
        print("Задача не найдена")
    else:
        column = fetch_from_db(Entities.COLUMN, column_code_or_id)
        if column is None:
            print("Колонка не найдена")
        else:
            update_in_db(Entities.TASK, task.id, {"column_id": column.id})
            print("Задача перемещена")


@app.command()
def create_column():
    column_values = ask_questions(COLUMN_INPUT_FIELDS_AND_VALIDATORS, Entities.COLUMN)
    save_to_db(Column(**column_values))


@app.command()
def update_column(column_code_or_id: str) -> None:
    print("Сделать вывод карточки")
    new_column_values = ask_questions(COLUMN_INPUT_FIELDS_AND_VALIDATORS, Entities.COLUMN)
    column = fetch_from_db(Entities.COLUMN, column_code_or_id)
    if column is None:
        print("Колонка не найдена")
    else:
        update_in_db(Entities.COLUMN, column.id, new_column_values)
        print("Колонка изменена")


@app.command()
def delete_column(column_code_or_id: str):
    column = fetch_from_db(Entities.COLUMN, column_code_or_id)
    if column is None:
        print("Колонка не найдена")
    else:
        update_in_db(Entities.COLUMN, column.id, {"is_delete": True})
        print("Колонка удалена")


if __name__ == "__main__":
    app()
