import typer
from rich import print
from rich.layout import Layout
from rich.panel import Panel

from kanban.column.changers import save_to_db as column_save, fetch_from_db as column_fetch, \
    update_in_db as column_update, get_undeleted_by_sort
from kanban.task.changers import save_to_db as task_save, fetch_from_db as task_fetch, \
    update_in_db as task_update
from kanban.column.utils import INPUT_FIELDS_AND_VALIDATORS as COLUMN_INPUTS
from kanban.task.utils import INPUT_FIELDS_AND_VALIDATORS as TASK_INPUTS, get_task_layouts
from kanban.db_models import Column, Task
from kanban.enums import InputEntities
from kanban.utils import get_user_input_values

app = typer.Typer()


@app.command()
def show():
    layout = Layout()
    panels = []
    columns = get_undeleted_by_sort()
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
    columns = get_undeleted_by_sort()
    if len(columns) == 0:
        raise RuntimeError("Колонки не найдены, создайте хотя бы одну")
    task_values = get_user_input_values(TASK_INPUTS, InputEntities.TASK)
    task_values["column_id"] = columns[0].id
    task_save(Task(**task_values))


@app.command()
def update(code_or_id: str):
    print("Сделать вывод карточки")
    new_task_values = get_user_input_values(TASK_INPUTS, InputEntities.TASK)
    task = task_fetch(code_or_id)
    if task is None:
        print("Задача не найдена")
    else:
        task_update(task.id, new_task_values)
        print("Задача изменена")


@app.command()
def delete(code_or_id: str):
    task = task_fetch(code_or_id)
    if task is None:
        print("Задача не найдена")
    else:
        task_update(task.id, {"is_delete": True})
        print("Задача удалена")


@app.command()
def move(code_or_id: str, column_code_or_id: str):
    task = task_fetch(code_or_id)
    if task is None:
        print("Задача не найдена")
    else:
        column = column_fetch(column_code_or_id)
        if column is None:
            print("Колонка не найдена")
        else:
            task_update(task.id, {"column_id": column.id})
            print("Задача перемещена")


@app.command()
def create_column():
    column_values = get_user_input_values(COLUMN_INPUTS, InputEntities.COLUMN)
    column_save(Column(**column_values))


@app.command()
def update_column(column_code_or_id: str) -> None:
    print("Сделать вывод карточки")
    new_column_values = get_user_input_values(COLUMN_INPUTS, InputEntities.COLUMN)
    column = column_fetch(column_code_or_id)
    if column is None:
        print("Колонка не найдена")
    else:
        column_update(column.id, new_column_values)
        print("Колонка изменена")


@app.command()
def delete_column(column_code_or_id: str):
    column = column_fetch(column_code_or_id)
    if column is None:
        print("Колонка не найдена")
    else:
        column_update(column.id, {"is_delete": True})
        print("Колонка удалена")


if __name__ == "__main__":
    app()
