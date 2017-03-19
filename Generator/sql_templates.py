class Statements:


    CREATE_STATEMENT = '''
CREATE TABLE "{table_name}" (
    {table_name}_id SERIAL PRIMARY KEY,
    {table_name}_created INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER),
{columns}
    {table_name}_updated INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER)
);
'''

    FUNCTION_UPDATED = '''
CREATE OR REPLACE FUNCTION update_{table_name}_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.{table_name}_updated = cast(extract(epoch from now()) AS INTEGER);
    RETURN NEW;
END;
$$ language \'plpgsql\';
'''

    TRIGGER_UPDATED = '''
CREATE TRIGGER \"{table_name}_update\"
BEFORE UPDATE
ON {table_name}
FOR EACH ROW
EXECUTE PROCEDURE update_{table_name}_timestamp();
'''

    ALTER_STATEMENT = '''
ALTER TABLE "{child}"
{references};
'''
    ADD_COLUMN = 'ADD COLUMN {parrent}_id INTEGER REFERENCES {parrent}({parrent}_id)'

    CREATE_JUNCTION_TABLE = '''
CREATE TABLE \"{0}_{1}\" (
    {0}_id INTEGER REFERENCES {0}({0}_id),
    {1}_id INTEGER REFERENCES {1}({1}_id)
);
'''

