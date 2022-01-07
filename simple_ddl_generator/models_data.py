from typing import Dict
from simple_ddl_generator.type_converter import prepare_type


def default_cleaner(default_value: str):
    if default_value:
        if 'datetime.' in default_value:
            default_value = default_value.split('datetime.')[-1]
    return default_value


def prepare_models_data(data: Dict):
    for table in data["tables"]:
        for column in table.columns:
            column.type = prepare_type(column.type)
            column.default = default_cleaner(column.default)
    return data