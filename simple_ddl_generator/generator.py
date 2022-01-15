import pathlib

from jinja2 import Environment, FileSystemLoader
from table_meta.model import TableMeta

templates_dir = pathlib.Path(__file__).parents[0] / "templates"

jinja2_env = Environment(loader=FileSystemLoader(templates_dir))


hql_table_properties = [
    "location",
    "row_format",
    "fields_terminated_by",
    "lines_terminated_by",
    "map_keys_terminated_by",
    "collection_items_terminated_by",
    "stored_as",
]


class Generator:
    def __init__(self, data: TableMeta, dialect: str, lowercase: bool = False) -> None:
        self.data = data
        self.dialect = dialect
        self.lowercase = lowercase

    def render_template(self) -> str:
        template = jinja2_env.get_template("common.jinja2")
        print(self.data)
        return template.render(
            lower=self.lowercase, properties_as_is=hql_table_properties, **self.data
        )
