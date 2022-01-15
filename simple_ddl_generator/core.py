from typing import Dict

from table_meta import TableMeta, ddl_to_meta, models_to_meta

from simple_ddl_generator.generator import Generator
from simple_ddl_generator.models_data import prepare_models_data


class DDLGenerator:
    def __init__(
        self, data: Dict, dialect: str = "sql", lowercase: bool = False
    ) -> None:
        self.data = data
        self.ddl_output = None
        self.dialect = dialect
        self.lowercase = lowercase

    def convert_to_table_meta(self):

        if not isinstance(self.data, dict) or not isinstance(
            self.data["tables"][0], TableMeta
        ):
            if isinstance(self.data, dict) and "attrs" not in self.data["tables"][0]:
                self.prepared_data = ddl_to_meta(self.data)
            else:
                self.prepare_models_data()
        else:
            self.prepared_data = self.data

    def prepare_models_data(self):
        self.prepared_data = prepare_models_data(models_to_meta(self.data))

    def generate(self) -> str:
        self.convert_to_table_meta()
        self.generate_ddl()

        return self.ddl_output

    def to_file(self, file_name) -> None:
        """saves ddl to file"""
        self.generate()
        with open(file_name, "w+") as target_file:
            target_file.write(self.ddl_output)

    def generate_ddl(self) -> str:
        self.result = Generator(
            self.prepared_data, self.dialect, self.lowercase
        ).render_template()
        return self.result
