from dateutil import parser

from kanban.enums import InputEntities
from kanban.validator import Validator, BOOLEAN_SYMBOLS


def get_user_input_values(dict_inputs: dict[str], input_entity_type: InputEntities) -> dict:
    column_values = {}
    for user_input in dict_inputs:
        is_valid = False
        while not is_valid:
            value = input(f"Please input {user_input}: ")
            is_valid = Validator(
                value=value,
                validate_types=dict_inputs[user_input],
                input_entity_type=input_entity_type,
            ).validate()
            print(is_valid)
            if is_valid:
                if "bool" in dict_inputs[user_input]:
                    value = BOOLEAN_SYMBOLS[value]
                if "datetime" in dict_inputs[user_input]:
                    value = parser.parse(value)
                column_values[user_input] = value
    return column_values
