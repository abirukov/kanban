from dataclasses import dataclass
from typing import Any

import dateutil
from dateutil import parser

from kanban.constants import BOOLEAN_SYMBOLS
from kanban.enums import Colors, Entities
from kanban.utils import fetch_from_db


@dataclass
class Validator:
    value: Any
    validate_types: str
    input_entity_type: Entities

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
        return len(self.value) > 0

    def validate_code(self, db_entity: Entities) -> bool:
        entity = fetch_from_db(self.value, db_entity)
        return entity is None

    def validate_datetime(self) -> bool:
        try:
            parser.parse(self.value)
            return True
        except dateutil.parser.ParserError:
            return False
