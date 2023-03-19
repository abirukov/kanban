from dataclasses import dataclass
from typing import Any

import dateutil
from dateutil import parser

from kanban.column.changers import fetch_from_db as column_fetch_from_db
from kanban.task.changers import fetch_from_db as task_fetch_from_db
from kanban.enums import Colors, InputEntities

BOOLEAN_SYMBOLS = {
    "1": True,
    "y": True,
    "Y": True,
    "0": False,
    "n": False,
    "N": False,
}

VALIDATE_ERROR_DESCRIPTIONS = {
    "code": "Код уже используется или совпадает с существующим id",
    "int": "Введите целое число",
    "bool": "Поддерживается ввод Y, y, 1, N, n, 0",
    "datetime": "Введите дату или время в свободной форме",
    "required|str": "Обязательное значение",
}


@dataclass
class Validator:
    value: Any
    validate_types: str
    input_entity_type: InputEntities

    def validate(self) -> bool:
        last_validate_result = True
        validate_types_list = self.validate_types.split("|")
        for validate_type in validate_types_list:
            method_name = 'validate_' + validate_type
            method = getattr(self, method_name)
            validate_result = method() and last_validate_result
        return validate_result

    def validate_str(self) -> bool:
        return isinstance(self.value, str)

    def validate_int(self) -> bool:
        try:
            int(self.value)
            return isinstance(self.value, str)
        except ValueError:
            return False

    def validate_color(self) -> bool:
        colors = [color.value for color in Colors]
        return self.value in colors

    def validate_bool(self) -> bool:
        return self.value in BOOLEAN_SYMBOLS.keys()

    def validate_required(self) -> bool:
        return self.value is not None

    def validate_code(self) -> bool:
        if self.input_entity_type == InputEntities.COLUMN:
            entity = column_fetch_from_db(self.value)
        else:
            entity = task_fetch_from_db(self.value)
        return entity is None

    def validate_datetime(self) -> bool:
        try:
            parser.parse(self.value)
            return True
        except dateutil.parser.ParserError:
            return False
