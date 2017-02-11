import psycopg2
import psycopg2.extras

class DatabaseError(Exception):
    pass


class NotFoundError(Exception):
    pass


class Entity(object):
    db = psycopg2.connect('dbname=test_database user=test_user password=qwerty')

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
        if self.__id is not None:
            self.__load()

        if name in self._columns:
            if self.__modified:
                raise DatabaseError
            return self.__fields[self.__table+'_'+ name]

    def __setattr__(self, name, value):
        if name in self._columns:
            if self.__id is not None:
                self.__load()
            column_name = self.__table + '_' + name
            self.__fields[column_name] = value
            self.__modified = True
        else:
            object.__setattr__(self, name, value)

    def __execute_query(self, query, args):
        query_result = self.__cursor.execute(query, args)
        self.__class__.db.commit()
        return query_result

    def __insert(self):
        placeholders = []
        for field in self.__fields.keys():
            placeholders.append('%({field})s'.format(field=field))

        insert_query = self.__insert_query.format(
            table=self.__table,
            columns=','.join(self.__fields.keys()),
            placeholders=','.join(placeholders)
        )
        self.__id = self.__execute_query(insert_query, self.__fields)

    def __load(self):
        if self.__loaded:
            return
        if self.__id is None:
            raise DatabaseError()

        self.__cursor.execute(self.__select_query.format(table=self.__table) % self.__id)
        result = self.__cursor.fetchone()

        if result is None:
            raise NotFoundError()

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
        self.__load()
        return self.__fields[name]
        # return value from fields array by <table>_<name> as a key
        pass

    def _set_column(self, name, value):
        self.__load()
        self.__fields[name] = value
        # put new value into fields array with <table>_<name> as a key

    @classmethod
    def all(cls):
        instances = []

        cursor = cls.db.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )
        query = cls.__list_query.format(table=cls.__name__.lower())
        result = cursor.execute(query)

        # get ALL rows with ALL columns from corrensponding table
        # for each row create an instance of appropriate class
        # each instance must be filled with column data, a correct id and MUST NOT query a database for own fields any more
        # return an array of istances
        pass

    def delete(self):
        if self.__id is None:
            raise DatabaseError
        query = self.__class__.__delete_query.format(
            table=self.__table
        ) % self.__id
        self.__cursor.execute(query)

    @property
    def id(self):
        return self.__id
        pass

    @property
    def created(self):
        return self.__fields['created']

    @property
    def updated(self):
        return self.__fields['updated']

    def save(self):
        if self.__id is None:
            self.__insert()
        else:
            self.__update()
        self.__modified = False
