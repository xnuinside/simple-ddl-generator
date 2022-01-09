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
updated_at DATETIME);
"""
    assert expected == g.result


def test_enum_generated():

    model_from = """
    class MaterialType(str, Enum):

        article = 'article'
        video = 'video'


    @dataclass
    class Material:

        id: int
        description: str = None
        additional_properties: Union[dict, list, tuple, anything] = None
        created_at: datetime.datetime = datetime.datetime.now()
        updated_at: datetime.datetime = None

    @dataclass
    class Material2:

        id: int
        description: str = None
        additional_properties: Union[dict, list] = None
        created_at: datetime.datetime = datetime.datetime.now()
        updated_at: datetime.datetime = None

        """
    result = parse(model_from)

    g = DDLGenerator(result)
    g.generate()

    expected = """CREATE TYPE MaterialType AS ENUM  ('article','video');

CREATE TABLE Material (
id INTEGER,
description VARCHAR DEFAULT NULL,
additional_properties JSON DEFAULT NULL,
created_at DATETIME DEFAULT now(),
updated_at DATETIME DEFAULT NULL);

CREATE TABLE Material2 (
id INTEGER,
description VARCHAR DEFAULT NULL,
additional_properties JSON DEFAULT NULL,
created_at DATETIME DEFAULT now(),
updated_at DATETIME DEFAULT NULL);
"""
    assert expected == g.result
