from simple_ddl_parser import DDLParser

from simple_ddl_generator import DDLGenerator


def test_no_unexpected_logs(capsys):

    ddl = """
    CREATE EXTERNAL TABLE test (
    test STRING NULL COMMENT 'xxxx',
    )
    PARTITIONED BY (snapshot STRING, cluster STRING)
    """

    parser = DDLParser(ddl)

    result = parser.run(output_mode="hql", group_by_type=True)
    g = DDLGenerator(result)
    g.generate()
    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""
