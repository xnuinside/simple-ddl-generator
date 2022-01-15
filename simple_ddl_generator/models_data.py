from typing import Dict, List

from simple_ddl_generator.type_converter import prepare_type


def default_cleaner(default_value: str) -> str:
    if default_value:
        if "datetime." in default_value:
            default_value: str = default_value.split("datetime.")[-1]
        elif default_value == "None":
            default_value = "NULL"
    return default_value


def prepare_enum_values(attrs: List[Dict]) -> List:
    # attrs in python enum - ENUM values
    values: List = []
    for attr in attrs:
        values.append(attr["default"])
    return values


def prepare_models_data(data: Dict) -> Dict:
    for table in data["tables"]:
        for column in table.columns:
            column.type = prepare_type(column.type, column)
            column.default = default_cleaner(column.default)
    for _type in data["types"]:
        if _type.base_type.upper() == "ENUM":
            _type.properties["values"] = prepare_enum_values(_type.attrs)
    return data
