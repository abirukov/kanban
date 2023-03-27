from typing import Any

import dateutil
from dateutil import parser

from kanban.constants import BOOLEAN_SYMBOLS
from kanban.db_models import Entities
from kanban.db_utils import fetch_from_db
from kanban.enums import Colors


def validate_str(value: Any) -> bool:
    return isinstance(value, str)


def validate_int(value: Any) -> bool:
    try:
        int_value = int(value)
        return isinstance(int_value, int)
    except ValueError:
        return False


def validate_color(value: Any) -> bool:
    colors = [color.value for color in Colors]
    return value in colors


def validate_bool(value: Any) -> bool:
    return value in BOOLEAN_SYMBOLS


def validate_required(value: Any) -> bool:
    if isinstance(value, str):
        return len(value) > 0
    else:
        return type(value) is None


def validate_code(value: Any, db_entity: Entities) -> bool:
    entity = fetch_from_db(db_entity, value)
    return entity is None


def validate_datetime(value: Any) -> bool:
    try:
        parser.parse(value)
        return True
    except dateutil.parser.ParserError:
        return False


def validate(value: Any, validate_types: str, input_entity_type: Entities) -> bool:
    validate_variants = {
        "str": validate_str(value),
        "int": validate_int(value),
        "color": validate_color(value),
        "bool": validate_bool(value),
        "required": validate_required(value),
        "code": validate_code(value, input_entity_type),
        "datetime": validate_datetime(value),
    }

    last_validate_result = True
    validate_types_list = validate_types.split("|")
    for validate_type in validate_types_list:
        if validate_type in validate_variants.keys():
            validate_result = validate_variants[validate_type] and last_validate_result
    return validate_result
