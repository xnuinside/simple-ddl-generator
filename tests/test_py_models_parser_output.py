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


def test_references_from_django():
    expected = """CREATE TABLE Publication (
title VARCHAR);

CREATE TABLE Article (
headline VARCHAR,
publications INTEGER FOREIGN KEY REFERENCES Publication);
"""

    model_from = """
from django.db import models

    class Publication(models.Model):
        title = models.CharField(max_length=30)

        class Meta:
            ordering = ['title']

        def __str__(self):
            return self.title

    class Article(models.Model):
        headline = models.CharField(max_length=100)
        publications = models.ManyToManyField(Publication)

        class Meta:
            ordering = ['headline']

        def __str__(self):
            return self.headline
    """
    result = parse(model_from)

    g = DDLGenerator(result)
    g.generate()

    assert g.result == expected


def test_primary_key_and_unique():
    models_str = """
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

        def __repr__(self):
            return '<User %r>' % self.username
    """
    result = parse(models_str)

    g = DDLGenerator(result)
    g.generate()
    expected = """CREATE TABLE User (
id db.Integer PRIMARY KEY,
username db.String(80) UNIQUE,
email db.String(120) UNIQUE);
"""
    expected == g.result


def test_lowercase():
    expected = """CREATE TABLE person (
id db.Integer PRIMARY KEY,
name db.String(50) NOT NULL,
addresses 'Address');

CREATE TABLE address (
id db.Integer PRIMARY KEY,
email db.String(120) NOT NULL,
person_id db.Integer NOT NULL);
"""

    models_str = """
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    addresses = db.relationship('Address', backref='person', lazy=True)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)
"""
    result = parse(models_str)

    g = DDLGenerator(result, lowercase=True)
    g.generate()
    assert g.result == expected
