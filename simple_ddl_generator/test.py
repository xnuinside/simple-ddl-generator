from simple_ddl_generator import DDLGenerator
from simple_ddl_parser import DDLParser

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
data = DDLParser(ddl).run(group_by_type=True, output_mode="bigquery")
g = DDLGenerator(data)
g.generate()
print(g.result)