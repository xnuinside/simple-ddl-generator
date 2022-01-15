from typing import Dict

from table_meta.model import Column

uuid_types = ("uuid", "uuid4", "uuid1")
arrays_types = (
    "list",
    "tuple",
    "set",
)

string_types = (
    "str",
    "varchar",
    "character",
    "character_vying",
    "varying",
    "char",
    "string",
    "String",
)

text_types = "text"
datetime_types = (
    "time",
    "datetime.datetime",
    "datetime",
    "datetime.date",
    "date",
)

json_types = ("union[dict, list]", "json", "union")
jsonb_types = ("jsonb",)

integer_types = ("integer", "int", "serial")

big_integer_types = ("bigint", "bigserial")

float_types = ("float",)

numeric_types = ("decimal", "numeric", "double")

boolean_types = ("boolean", "bool")

timestamp_types = ("timestamp", "datetime.time")
datetime_types = (
    "DATETIME",
    "DATE",
    "datetime.datetime",
    "datetime",
    "datetime.date",
    "date",
)

models_types_mapping = {
    string_types: "VARCHAR",
    datetime_types: "DATETIME",
    integer_types: "INTEGER",
    boolean_types: "BOOLEAN",
    timestamp_types: "TIMESTAMP",
    big_integer_types: "BIGINTEGER",
    json_types: "JSON",
    jsonb_types: "JSONB",
    uuid_types: "UUID",
    arrays_types: "ARRAY",
}


def populate_types_mapping(mapper: Dict) -> Dict:
    types_mapping = {}
    for type_group, value in mapper.items():
        for type_ in type_group:
            types_mapping[type_] = value
    return types_mapping


def prepare_type(_type: str, column: Column) -> str:
    if "Optional" in _type:
        # python Optional type
        _type = _type.split("Optional[")[1].replace("]", "")
    column_data_type = _type.split("[")[0]

    for type_collection, mapped_value in models_types_mapping.items():
        if column_data_type.lower() in type_collection:
            return mapped_value

    return column_data_type
