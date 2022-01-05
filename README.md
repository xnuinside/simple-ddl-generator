## Simple DDL Generator

![badge1](https://img.shields.io/pypi/v/simple-ddl-generator) ![badge2](https://img.shields.io/pypi/l/simple-ddl-generator) ![badge3](https://img.shields.io/pypi/pyversions/simple-ddl-generator) ![workflow](https://github.com/xnuinside/simple-ddl-generator/actions/workflows/main.yml/badge.svg)

## What is it?

Simple DDL Generator generate SQL DDL from 3 different inputs. Idea of the generator same as for parser to support as much as possible DDLs in future.

Simple DDL Generator generate SQL DDL from 3 input formats - 1st from output Simple DDL Parser (https://github.com/xnuinside/simple-ddl-parser), 2nd from py-models-parser - https://github.com/xnuinside/py-models-parser. Or you can directly pass TableMeta classes (https://github.com/xnuinside/table-meta) to generator

## How to use

As usually - more samples in tests/ 

```bash

    pip install simple-ddl-generator

```


```python

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

```


## Changelog
**v0.1.0**

Base Generator Functionality with several test cases.
