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
        serial_key = '{table_name}_id SERIAL PRIMARY KEY'
        created_timestamp = '{table_name}_created INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER'
        updated_timestamp = '{table_name}_updated INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER'

        for table_name, table_structure in yaml_object.items():
            table_name = table_name.lower()
            create_statement = 'CREATE TABLE \"{table_name}\" (\n{fields});'
            fields = [serial_key.format(table_name=table_name),
                      created_timestamp.format(table_name=table_name),
                      updated_timestamp.format(table_name=table_name)]

            for fields_data in table_structure.values():
                for field_name, field_type in fields_data.items():
                    fields.append('\t{table_name}_{field_name} {field_type}'
                                  .format(table_name=table_name, field_name=field_name, field_type=field_type))

            fields = ','.join(fields)
            self.__statements.append(create_statement.format(table_name=table_name, fields=fields))
            self.__generate_created_timpestamp_functions(table_name)
            self.__generate_trigger_timestamp_updated(table_name)
        return self.__statements



    def __generate_created_timpestamp_functions(self, table_name):
        function_timestamp_created = 'CREATE OR REPLACE FUNCTION {1}_{0}_timestamp()\n' \
                                     'RETURNS TRIGGER AS $$\n' \
                                     'BEGIN\n' \
                                       'NEW.{0}_{1}d = now();\n' \
                                       'RETURN NEW;\n' \
                                     'END;\n' \
                                     '$$ language \'plpgsql\';\n'

        self.__statements.append(function_timestamp_created.format(table_name, 'create'))
        self.__statements.append(function_timestamp_created.format(table_name, 'update'))

    def __generate_trigger_timestamp_created(self, table_name):
        trigger_timestamp_created = 'CREATE TRIGGER \"{0}_created\"\n' \
                                    'AFTER INSERT\n' \
                                    'ON {0}\n' \
                                    'FOR EACH ROW\n' \
                                    'EXECUTE PROCEDURE create_{0}_timestamp;\n' \

        self.__statements.append(trigger_timestamp_created.format(table_name))

    def __generate_trigger_timestamp_updated(self, table_name):
        trigger_timestamp_updated = 'CREATE TRIGGER \"{0}_created\"\n' \
                                    'BEFORE UPDATE\n' \
                                    'ON {0}\n' \
                                    'FOR EACH ROW\n' \
                                    'EXECUTE PROCEDURE update_{0}_timestamp;\n'

        self.__statements.append(trigger_timestamp_updated.format(table_name))

    # def __generate_updated_timestamp_function(self, table_name):
    #     function_timestamp_created = 'CREATE OR REPLACE FUNCTION update_{0}_timestamp()' \
    #                                  'RETURNS TRIGGER AS $$' \
    #                                  'BEGIN' \
    #                                    'NEW.{0}_updated = now();' \
    #                                    'RETURN NEW;' \
    #                                  'END;' \
    #                                  '$$ language \'plpgsql\'' \
    #                                  .format(table_name)



