
Simple DDL Generator
--------------------


.. image:: https://img.shields.io/pypi/v/simple-ddl-generator
   :target: https://img.shields.io/pypi/v/simple-ddl-generator
   :alt: badge1
 
.. image:: https://img.shields.io/pypi/l/simple-ddl-generator
   :target: https://img.shields.io/pypi/l/simple-ddl-generator
   :alt: badge2
 
.. image:: https://img.shields.io/pypi/pyversions/simple-ddl-generator
   :target: https://img.shields.io/pypi/pyversions/simple-ddl-generator
   :alt: badge3
 
.. image:: https://github.com/xnuinside/simple-ddl-generator/actions/workflows/main.yml/badge.svg
   :target: https://github.com/xnuinside/simple-ddl-generator/actions/workflows/main.yml/badge.svg
   :alt: workflow


What is it?
-----------

Simple DDL Generator generate SQL DDL from 3 different inputs. Idea of the generator same as for parser to support as much as possible DDLs in future.

Simple DDL Generator generate SQL DDL from 3 input formats - 1st from output Simple DDL Parser (https://github.com/xnuinside/simple-ddl-parser), 2nd from py-models-parser - https://github.com/xnuinside/py-models-parser. Or you can directly pass TableMeta classes (https://github.com/xnuinside/table-meta) to generator

Generate DDL from Django, SQLAlchemy, Dataclasses, Pydantic models and other
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generator can generate DDL from all models that supported & parsed by https://github.com/xnuinside/py-models-parser.

If you need DDL generation from another Python Model types - open issue request to add support for this models in parser. 

How to use
----------

As usually - more samples in tests/ 

.. code-block:: bash


       pip install simple-ddl-generator

Generate / Modify using existed DDL with Simple-DDL-Parser
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sample how you can modify your DDL using Simple DDL Parser & Simple DDL Parser

.. code-block:: python


       from simple_ddl_generator import DDLGenerator
       from simple_ddl_parser import DDLParser

       # take initial DDL
       ddl = """CREATE EXTERNAL TABLE IF NOT EXISTS database.table_name
           (
               day_long_nm     string,
               calendar_dt     date,
               source_batch_id string,
               field_qty       decimal(10, 0),
               field_bool      boolean,
               field_float     float,
               create_tmst     timestamp,
               field_double    double,
               field_long      bigint
           ) PARTITIONED BY (batch_id int);"""
       # get result from parser
       data = DDLParser(ddl).run(group_by_type=True, output_mode="bigquery")

       # rename, for example, table name

       data["tables"][0]["table_name"] = "new_table_name"
       g = DDLGenerator(data)
       g.generate()
       print(g.result)

       # and result will be:

       """
       CREATE EXTERNAL TABLE "database.new_table_name" (
       day_long_nm string,
       calendar_dt date,
       source_batch_id string,
       field_qty decimal(10, 0),
       field_bool boolean,
       field_float float,
       create_tmst timestamp,
       field_double double,
       field_long bigint)
       PARTITIONED BY (batch_id int);
       """

Generate DDL from various Python Models with py-models-parser
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python


       from simple_ddl_generator import DDLGenerator
       from py_models_parser import parse

       # you can also read them from file
       model_from = """
           class Material(BaseModel):

               id: int
               title: str
               description: Optional[str]
               link: str = 'http://'
               type: Optional[MaterialType]
               additional_properties: Optional[Json]
               created_at: Optional[datetime.datetime] = datetime.datetime.now()
               updated_at: Optional[datetime.datetime]
           """
       # get data with parser
       result = parse(model_from)

       # if you want lower case table name before DDL generation you can just change in the result metadata, like this:
       # result[0].table_name = "material"
       # pass data to DDL Generator
       g = DDLGenerator(result)
       g.generate()
       print(g.result)  

       # resul will be

       """CREATE TABLE "Material" (
   id INTEGER,
   title VARCHAR,
   description VARCHAR,
   link VARCHAR DEFAULT 'http://',
   type MaterialType,
   additional_properties JSON,
   created_at DATETIME DEFAULT now(),
   updated_at DATETIME);
   """

Generate DDL Enum types from Python Enum & DDLs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now parser also generate CREATE TYPE statements.

For example (sample for generation DDL from Dataclasses):

.. code-block:: python


       from simple_ddl_generator import DDLGenerator
       from py_models_parser import parse

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
       print(g.result)

   # result will be:

   """CREATE TYPE MaterialType AS ENUM  ('article','video');

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

Changelog
---------

**v0.4.0**
New Features:


#. Added base support for REFERENCE statement generation
#. Added UNIQUE to column
#. Added PRIMARY KEY to column
#. To DDLGenerator added param lowercase to lowercase tables name.

**v0.3.0**
New Features:


#. Added CREATE TYPE generation from Python Enum & simple-ddl-parser types metadata

Improvements:


#. Added more test cases with models into tests
#. Now output generated with empty line at the end

Fixes:


#. Fixed issue with "" in names if quotes already exists in table-name in metadata

**v0.2.0**


#. Updated parser version in tests.
#. Added support for EXTERNAL & IF NOT EXISTS statetements.
#. Added support for using py-models-parser output as input and added sample in README.md:

DDL Generation from Pydantic, SQLAlchemy and other python models.

**v0.1.0**

Base Generator Functionality with several test cases.
