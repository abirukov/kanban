COLUMN_INPUT_FIELDS_AND_VALIDATORS = {
    "code": "code",
    "title": "required|str",
    "color": "color",
    "sort": "int",
}

TASK_INPUT_FIELDS_AND_VALIDATORS = {
    "code": "code",
    "title": "required|str",
    "is_important": "bool",
    "description": "str",
    "deadline": "datetime",
}

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
