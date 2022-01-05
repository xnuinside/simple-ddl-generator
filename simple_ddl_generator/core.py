from table_meta import ddl_to_meta
from typing import Dict
from simple_ddl_generator.generator import Generator


class DDLGenerator:
    
    def __init__(self, data: Dict, dialect: str = 'sql') -> None:
        self.data = data
        self.ddl_output = None
        self.dialect = dialect
        
    def generate(self) -> str:
        self.tables = ddl_to_meta(self.data)
        self.generate_ddl()
        return self.ddl_output
    
    def to_file(self, file_name) -> None:
        """ saves ddl to file """
        self.generate()
        with open(file_name, 'w+') as target_file:
            target_file.write(self.ddl_output)

    def generate_ddl(self) -> str:
        self.result = Generator(self.tables, self.dialect).render_template()
        return self.result
