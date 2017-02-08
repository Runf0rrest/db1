import psycopg2
import psycopg2.extras

class DatabaseError(Exception):
    pass


class NotFoundError(Exception):
    pass


class Entity(object):
    db = psycopg2.connect('dbname=test_database user=test_user')

    # ORM part 1
    __delete_query    = 'DELETE FROM "{table}" WHERE {table}_id=%s'
    __insert_query    = 'INSERT INTO "{table}" ({columns}) VALUES ({placeholders}) RETURNING "{table}_id"'
    __list_query      = 'SELECT * FROM "{table}"'
    __select_query    = 'SELECT * FROM "{table}" WHERE {table}_id=%s'
    __update_query    = 'UPDATE "{table}" SET {columns} WHERE {table}_id=%s'

    def __init__(self, id=None):
        if self.__class__.db is None:
            raise DatabaseError()

        self.__cursor   = self.__class__.db.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )
        self.__fields   = {}
        self.__id       = id
        self.__loaded   = False
        self.__modified = False
        self.__table    = self.__class__.__name__.lower()

    def __getattr__(self, name):
        if self.__modified:
            raise DatabaseError

        self.__load()

        # check, if instance is modified and throw an exception
        # get corresponding data from database if needed
        # check, if requested property name is in current class
        #    columns, parents, children or siblings and call corresponding
        #    getter with name as an argument
        # throw an exception, if attribute is unrecognized
        pass

    def __setattr__(self, name, value):
        # check, if requested property name is in current class
        #    columns, parents, children or siblings and call corresponding
        #    setter with name and value as arguments or use default implementation
        pass

    def __execute_query(self, query, args):
        # execute an sql statement and handle exceptions together with transactions
        pass

    def __insert(self):
        # generate an insert query string from fields keys and values and execute it
        # use prepared statements
        # save an insert id
        pass

    def __load(self):
        if not self.__loaded:
            self.__cursor.execute(self.__select_query.format(table=self.__table) % self.__id)
            result = self.__cursor.fetchone()

            if result is None:
                raise NotFoundError

            self.__loaded = True
            self.__fields = result

    def __update(self):
        # generate an update query string from fields keys and values and execute it
        # use prepared statements
        pass

    def _get_children(self, name):
        children = []

        # return an array of child entity instances
        # each child instance must have an id and be filled with data
        pass

    def _get_column(self, name):
        # return value from fields array by <table>_<name> as a key
        pass

    def _set_column(self, name, value):
        # put new value into fields array with <table>_<name> as a key
        pass

    @classmethod
    def all(cls):
        # get ALL rows with ALL columns from corrensponding table
        # for each row create an instance of appropriate class
        # each instance must be filled with column data, a correct id and MUST NOT query a database for own fields any more
        # return an array of istances
        pass

    def delete(self):
        # execute delete query with appropriate id
        pass

    @property
    def id(self):
        # try to guess yourself
        pass

    @property
    def created(self):
        # try to guess yourself
        pass

    @property
    def updated(self):
        # try to guess yourself
        pass

    def save(self):
        # execute either insert or update query, depending on instance id
        pass