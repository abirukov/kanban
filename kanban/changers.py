from db import DB_SESSION
from kanban.db_models import Column, Task
from kanban.enums import Entities


class Changer:
    def __init__(self, db_model_type: Entities):
        self.type = db_model_type.value

    @staticmethod
    def save_to_db(db_model: Column | Task) -> Column | Task:
        DB_SESSION.add(db_model)
        DB_SESSION.commit()
        return db_model

    def update_in_db(self, id: int, new_fields: dict) -> None:
        DB_SESSION.query(self.type).filter(
            self.type.id == id,
        ).update(
            new_fields, synchronize_session=False,
        )
        DB_SESSION.commit()

    def fetch_from_db_by_id(self, id: int) -> Column | Task | None:
        return self.type.query.filter(self.type.id == id).first()

    def fetch_from_db_by_code(self, code: str) -> Column | Task | None:
        return self.type.query.filter(self.type.code == code).first()

    def get_undeleted_by_sort(self) -> list[Column | Task | None]:
        return self.type.query.filter(
            self.type.is_delete.is_(False),
        ).order_by(
            self.type.sort.asc(),
        ).all()
