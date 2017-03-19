import yaml
from sql_templates import Statements
from collections import defaultdict
from sortedcontainers import SortedList

class Generator:
    
   
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__yaml_object = None
        self.__one_to_many = defaultdict(list)
        self.__many_to_many = []

    def __parse_file(self):
        with open(self.__file_path, 'r') as file:
            self.__yaml_object = yaml.safe_load(file)
            
    def __generate_columns(self, table_name):
        for column_name, colmn_type in self.__yaml_object[table_name]['fields'].items():
            yield '\t{0}_{1} {2},'.format(
                table_name.lower(),
                column_name,
                colmn_type
            )
    
    def __get_inverted_relation(self, table, related_table):
        return self.__yaml_object[related_table]['relations'][table]
    
    def __parse_relations(self, table):
        for related_table, relation in self.__yaml_object[table]['relations'].items():
            inverted_relation = self.__get_inverted_relation(table, related_table)
            
            if inverted_relation != 'many':
                continue
            if relation == 'one':
                self.__one_to_many[table.lower()].append(related_table.lower())
            elif relation == 'many':
                if (related_table, table) not in self.__many_to_many:
                    self.__many_to_many.append((table, related_table))
    
    def __generate_parrent_columns(self, parrents):
        for parrent in parrents:
            yield Statements.ADD_COLUMN.format(parrent=parrent)
     
    def __generate_one_to_many_relations(self):
        for child, parrents in self.__one_to_many.items():
            parrent_collumns = '\n'.join(self.__generate_parrent_columns(parrents))
            yield Statements.ALTER_STATEMENT.format(
                child=child,
                references=parrent_collumns
                )
        
    def __generate_many_to_many_relations(self):
        for relation in self.__many_to_many:
            yield Statements.CREATE_JUNCTION_TABLE.format(
                relation[0].lower(),
                relation[1].lower()
                )
    
    def generate(self):
        self.__parse_file()
        for table_name in self.__yaml_object.keys():
            name = table_name.lower()
            self.__parse_relations(table_name)
                            
            yield Statements.CREATE_STATEMENT.format(
                table_name=name,
                columns="\n".join(self.__generate_columns(table_name))
            )
            yield Statements.FUNCTION_UPDATED.format(
                table_name=name
            )
            yield Statements.TRIGGER_UPDATED.format(
                table_name=name
            )
        yield ''.join(self.__generate_one_to_many_relations())
        yield ''.join(self.__generate_many_to_many_relations())
