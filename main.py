import typer
from kanban.column.changers import save_to_db as column_save, fetch_from_db as column_fetch, \
    update_in_db as column_update, get_all_by_sort
from kanban.task.changers import save_to_db as task_save, fetch_from_db as task_fetch,\
    update_in_db as task_update
from kanban.column.utils import INPUT_FIELDS_AND_VALIDATORS as COLUMN_INPUTS
from kanban.task.utils import INPUT_FIELDS_AND_VALIDATORS as TASK_INPUTS
from kanban.db_models import Column, Task
from kanban.enums import InputEntities
from kanban.utils import get_user_input_values

app = typer.Typer()


@app.command()
def show():
    print("Show all")


@app.command()
def create():
    columns = get_all_by_sort()
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
