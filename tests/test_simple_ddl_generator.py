from simple_ddl_parser import DDLParser

from simple_ddl_generator import DDLGenerator


def test_simple_generation():
    expected = "CREATE TABLE new_table;\n"

    ddl = "create table new_table;"
    data = DDLParser(ddl).run(group_by_type=True, output_mode="bigquery")
    g = DDLGenerator(data)
    g.generate()
    assert expected == g.result


def test_partitioned_by():
    expected = """CREATE EXTERNAL TABLE IF NOT EXISTS database.new_table_name (
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
        ) PARTITIONED BY (batch_id int);
"""
    # get result from parser
    data = DDLParser(ddl).run(group_by_type=True, output_mode="hql")

    # rename, for example, table name

    data["tables"][0]["table_name"] = "new_table_name"
    g = DDLGenerator(data)
    g.generate()
    assert g.result == expected


def test_hql_several_more_properties():
    ddl = """CREATE TABLE IF NOT EXISTS default.salesorderdetail(
        SalesOrderID int,
        ProductID int,
        OrderQty int,
        LineTotal decimal
        )
    PARTITIONED BY (batch_id int, batch_id2 string, batch_32 some_type)
    LOCATION 's3://datalake/table_name/v1'
    ROW FORMAT DELIMITED
        FIELDS TERMINATED BY ','
        COLLECTION ITEMS TERMINATED BY '\002'
        MAP KEYS TERMINATED BY '\003'
    STORED AS TEXTFILE
    """
    # get result from parser
    data = DDLParser(ddl).run(group_by_type=True, output_mode="hql")

    # rename, for example, table name

    g = DDLGenerator(data)
    data["tables"][0]["location"] = "s3://new_location"
    g.generate()
    expected = r"""CREATE TABLE IF NOT EXISTS default.salesorderdetail (
SalesOrderID int,
ProductID int,
OrderQty int,
LineTotal decimal)
PARTITIONED BY (batch_id int, batch_id2 string, batch_32 some_type)
LOCATION s3://new_location
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
MAP KEYS TERMINATED BY '\003'
COLLECTION ITEMS TERMINATED BY '\002'
STORED AS TEXTFILE;
"""

    assert expected == g.result


def test_create_type():
    ddl = """
    CREATE TYPE "ContentType" AS
    ENUM ('TEXT','MARKDOWN','HTML');
    CREATE TABLE "schema--notification"."notification" (
        content_type "ContentType"
    );
    """

    # get result from parser
    data = DDLParser(ddl).run(group_by_type=True)

    # rename, for example, table name

    g = DDLGenerator(data)
    g.generate()
    expected = """CREATE TYPE "ContentType" AS ENUM  ('TEXT','MARKDOWN','HTML');

CREATE TABLE "schema--notification"."notification" (
content_type "ContentType");
"""
    assert expected == g.result
