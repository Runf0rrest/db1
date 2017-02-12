import psycopg2
import psycopg2.extras

class DatabaseError(Exception):
    pass

class EntityIsModifiedError(Exception):
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
                raise EntityIsModifiedError()
            return self._get_column(name)

    def __setattr__(self, name, value):
        if name in self._columns:
            if self.__id is not None:
                self.__load()
            self._set_column(name, value)
        else:
            object.__setattr__(self, name, value)

    def __execute_query(self, query, args):
        print(type(args))
        self.__cursor.execute(query, args)
        self.__class__.db.commit()

    def __insert(self):
        placeholders = []
        for field in self.__fields.keys():
            placeholders.append('%({field})s'.format(field=field))

        insert_query = self.__insert_query.format(
            table=self.__table,
            columns=','.join(self.__fields.keys()),
            placeholders=','.join(placeholders)
        )
        self.__execute_query(insert_query, self.__fields)
        self.__id = self.__cursor.fetchone()[0]


    def __load(self):
        if self.__loaded:
            return
        if self.__id is None:
            raise DatabaseError()

        query = self.__select_query.format(table=self.__table)
        self.__execute_query(query, [self.__id])
        result = self.__cursor.fetchone()

        if result is None:
            raise NotFoundError()

        self.__loaded = True
        self.__fields = dict(result)

    def __update(self):
        columns = []
        args = []
        for column_name in self._columns:
            col = self.__table + '_' + column_name + '=%s'
            args.append(str(self._get_column(column_name)))
            columns.append(col)
        args.append(str(self.__id))
        query = self.__update_query.format(
            table=self.__table,
            columns=','.join(columns)
        )
        self.__execute_query(query, args)

    def _get_column(self, name):
        self.__load()
        return self.__fields[self.__table + '_' + name]

    def _set_column(self, name, value):
        self.__fields[self.__table + '_' + name] = value
        self.__modified = True

    @classmethod
    def all(cls):
        instances = []
        cursor = cls.db.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )
        query = cls.__list_query.format(table=cls.__name__.lower())
        cursor.execute(query)
        result = cursor.fetchall()

        for column_values in result:
            instance = cls()
            for column_name, column_value in zip(cls._columns, column_values) :
                instance.__fields[column_name] = column_value
            instance.__loaded = True
            instances.append(instance)
            #instance.__id = instance.id
        return instances

    def delete(self):
        if self.__id is None:
            raise DatabaseError
        query = self.__class__.__delete_query.format(
            table=self.__table
        ) % self.__id
        self.__cursor.execute(query)

    @property
    def id(self):
        return self._get_column('id')

    @property
    def created(self):
        return self._get_column('created')

    @property
    def updated(self):
        return self._get_column('updated')

    def save(self):
        if self.__id is None:
            self.__insert()
        else:
            self.__update()
        self.__modified = False
        self.__load()
