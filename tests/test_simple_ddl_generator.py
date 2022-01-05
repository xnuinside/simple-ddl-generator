from simple_ddl_generator import DDLGenerator
from simple_ddl_parser import DDLParser


def test_simple_generation():
    expected = 'CREATE TABLE "new_table";'
        
    ddl = "create table new_table;"
    data = DDLParser(ddl).run(group_by_type=True, output_mode="bigquery")
    g = DDLGenerator(data)
    g.generate()
    assert expected == g.result


def test_partitioned_by():
    expected = """CREATE TABLE "database.new_table_name" (
day_long_nm string,
calendar_dt date,
source_batch_id string,
field_qty decimal(10, 0),
field_bool boolean,
field_float float,
create_tmst timestamp,
field_double double,
field_long bigint)
PARTITIONED BY (batch_id int);"""

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
    assert g.result == expected

