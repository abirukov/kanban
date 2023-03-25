import pytest

from db import DB_SESSION
from kanban.changers import Changer
from kanban.db_models import Entities


@pytest.mark.parametrize(
    "entity_type, model",
    [
        (Entities.COLUMN, pytest.lazy_fixture("start_column")),
        (Entities.TASK, pytest.lazy_fixture("test_task_saved")),
    ],
)
def test__save_to_db(entity_type, model):
    Changer(entity_type).save_to_db(model)

    model_in_db = Changer(entity_type).fetch_from_db(model.code)
    assert model == model_in_db
    entity_type.value.query.filter_by(id=model_in_db.id).delete()
    DB_SESSION.commit()


@pytest.mark.parametrize(
    "entity_type, saved_model",
    [
        (Entities.COLUMN, pytest.lazy_fixture("start_column_saved")),
        (Entities.TASK, pytest.lazy_fixture("test_task_saved")),
    ],
)
def test__update_in_db(entity_type, saved_model):
    Changer(entity_type).update_in_db(saved_model.id, {"title": "updated_title"})

    model_in_db = Changer(entity_type).fetch_from_db(saved_model.code)
    saved_model.title = "start_column_updated"
    assert saved_model == model_in_db


@pytest.mark.parametrize(
    "entity_type, saved_model",
    [
        (Entities.COLUMN, pytest.lazy_fixture("start_column_saved")),
        (Entities.TASK, pytest.lazy_fixture("test_task_saved")),
    ],
)
def test__fetch_from_db_by_id(entity_type, saved_model):
    model_in_db = Changer(entity_type).fetch_from_db_by_id(saved_model.id)
    assert saved_model == model_in_db


@pytest.mark.parametrize(
    "entity_type, saved_model",
    [
        (Entities.COLUMN, pytest.lazy_fixture("start_column_saved")),
        (Entities.TASK, pytest.lazy_fixture("test_task_saved")),
    ],
)
def test__fetch_from_db_by_code(entity_type, saved_model):
    model_in_db = Changer(entity_type).fetch_from_db_by_code(saved_model.code)
    assert saved_model == model_in_db


@pytest.mark.parametrize(
    "entity_type, saved_model",
    [
        (Entities.COLUMN, pytest.lazy_fixture("start_column_saved")),
        (Entities.TASK, pytest.lazy_fixture("test_task_saved")),
    ],
)
def test__fetch_from_db__code(entity_type, saved_model):
    model_in_db = Changer(entity_type).fetch_from_db(saved_model.code)
    assert saved_model == model_in_db


@pytest.mark.parametrize(
    "entity_type, saved_model",
    [
        (Entities.COLUMN, pytest.lazy_fixture("start_column_saved")),
        (Entities.TASK, pytest.lazy_fixture("test_task_saved")),
    ],
)
def test__fetch_from_db__id(entity_type, saved_model):
    model_in_db = Changer(entity_type).fetch_from_db(saved_model.id)
    assert saved_model == model_in_db


def test__get_undeleted_by_sort(start_column_saved, finish_column_saved):
    columns_list = Changer(Entities.COLUMN).get_undeleted_by_sort()
    assert columns_list == [start_column_saved, finish_column_saved]


@pytest.mark.parametrize(
    "entity_type, saved_model",
    [
        (Entities.COLUMN, pytest.lazy_fixture("start_column_saved")),
        (Entities.TASK, pytest.lazy_fixture("test_task_saved")),
    ],
)
def test_fetch_from_db(entity_type, saved_model):
    assert Changer(entity_type).fetch_from_db(saved_model.id)
