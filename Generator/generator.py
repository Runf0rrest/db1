import yaml


class Generator:

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__statements = []

    def __parse_file(self):
        file = open(self.__file_path)
        parsing_result = yaml.safe_load(file)

        file.close()

        return parsing_result

    def generate_statements(self):
        yaml_object = self.__parse_file()
        base_fields = '{table_name}_id SERIAL PRIMARY KEY,\n' \
                      '{table_name}_created INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER),\n' \
                      '{table_name}_updated INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER)'

        for table_name, table_structure in yaml_object.items():
            table_name = table_name.lower()
            create_statement = 'CREATE TABLE \"{table_name}\" (\n{fields}\n);\n'
            fields = [base_fields.format(table_name=table_name)]

            for fields_data in table_structure.values():
                for field_name, field_type in fields_data.items():
                    fields.append(',\n{table_name}_{field_name} {field_type}'
                                  .format(table_name=table_name, field_name=field_name, field_type=field_type))

            fields = ''.join(fields)
            self.__statements.append(create_statement.format(table_name=table_name, fields=fields))
            self.__generate_created_timpestamp_functions(table_name)
            self.__generate_trigger_timestamp_updated(table_name)
        return self.__statements

    def __generate_created_timpestamp_functions(self, table_name):
        function_timestamp_created = 'CREATE OR REPLACE FUNCTION update_{table_name}_timestamp()\n' \
                                     'RETURNS TRIGGER AS $$\n' \
                                     'BEGIN\n' \
                                       'NEW.{table_name}_updated = cast(extract(epoch from now()) AS INTEGER);\n' \
                                       'RETURN NEW;\n' \
                                     'END;\n' \
                                     '$$ language \'plpgsql\';\n'

        self.__statements.append(function_timestamp_created.format(table_name=table_name))

    def __generate_trigger_timestamp_updated(self, table_name):
        trigger_timestamp_updated = 'CREATE TRIGGER \"{table_name}_update\"\n' \
                                    'BEFORE UPDATE\n' \
                                    'ON {table_name}\n' \
                                    'FOR EACH ROW\n' \
                                    'EXECUTE PROCEDURE update_{table_name}_timestamp();\n'

        self.__statements.append(trigger_timestamp_updated.format(table_name=table_name))

