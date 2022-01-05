from simple_ddl_generator import DDLGenerator
from simple_ddl_parser import DDLParser


def test_simple_generation():
    expected = "CREATE TABLE new_table;"
        
    ddl = "create table new_table;"
    data = DDLParser(ddl).run(group_by_type=True, output_mode="bigquery")
    g = DDLGenerator(data)
    g.generate()
    assert expected == g.result
