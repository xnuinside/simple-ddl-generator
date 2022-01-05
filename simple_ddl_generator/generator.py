import pathlib
from table_meta.model import TableMeta
from jinja2 import Environment, FileSystemLoader

templates_dir = pathlib.Path(__file__).parents[0] / 'templates' 

jinja2_env = Environment(loader=FileSystemLoader(templates_dir))


hql_table_properties = ['location', 'row_format', 'fields_terminated_by', 
'lines_terminated_by', 'map_keys_terminated_by', 'collection_items_terminated_by', 'stored_as']


class Generator:
    
    def __init__(self, tables: TableMeta, dialect: str) -> None:
        self.tables = tables
        self.dialect = dialect
    
    def render_template(self) -> str:
        template = jinja2_env.get_template('common.jinja2')
        
        return template.render(
            properties_as_is=hql_table_properties,
            **self.tables)
