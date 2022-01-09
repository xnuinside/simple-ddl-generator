from py_models_parser import parse

from simple_ddl_generator import DDLGenerator


def test_ddl_from_pydantic_model():
    model_from = """class Material(BaseModel):
    id: int
    title: str
    description: Optional[str]
    link: str = 'http://'
    type: Optional[MaterialType]
    additional_properties: Optional[Json]
    created_at: Optional[datetime.datetime] = datetime.datetime.now()
    updated_at: Optional[datetime.datetime]"""
    result = parse(model_from)

    g = DDLGenerator(result)
    g.generate()
    expected = """CREATE TABLE Material (
id INTEGER,
title VARCHAR,
description VARCHAR,
link VARCHAR DEFAULT 'http://',
type MaterialType,
additional_properties JSON,
created_at DATETIME DEFAULT now(),
updated_at DATETIME);"""
    assert expected == g.result


def test_enum_generated():
    pass
