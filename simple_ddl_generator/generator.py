import pathlib
from table_meta.model import TableMeta
from jinja2 import Environment, FileSystemLoader

templates_dir = pathlib.Path(__file__).parents[0] / 'templates' 

jinja2_env = Environment(loader=FileSystemLoader(templates_dir))


class Generator:
    
    def __init__(self, tables: TableMeta, dialect: str) -> None:
        self.tables = tables
        self.dialect = dialect
    
    def render_template(self) -> str:
        template = jinja2_env.get_template('common.jinja2')
        print(self.tables)
        return template.render(**self.tables)
