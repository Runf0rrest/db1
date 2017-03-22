import psycopg2
import psycopg2.extras

class DatabaseError(Exception):
    pass

class EntityIsModifiedError(Exception):
    pass

class NotFoundError(Exception):
    pass


class Entity(object):
    db = None

    # ORM part 1
    __delete_query    = 'DELETE FROM "{table}" WHERE {table}_id=%s'
    __insert_query    = 'INSERT INTO "{table}" ({columns}) VALUES ({placeholders}) RETURNING "{table}_id"'
    __list_query      = 'SELECT * FROM "{table}"'
    __select_query    = 'SELECT * FROM "{table}" WHERE {table}_id=%s'
    __update_query    = 'UPDATE "{table}" SET {columns} WHERE {table}_id=%s'
    
    __parent_query    = 'SELECT * FROM "{table}" WHERE {parent}_id=%s'
    __sibling_query   = 'SELECT * FROM "{siblings}" NATURAL JOIN "{join_table}" WHERE {table}_id=%s'
    __update_children = 'UPDATE "{table}" SET {parent}_id=%s WHERE {table}_id IN ({children})'
    

    
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
        self.__cursor.execute(query, args)
        self.__class__.db.commit()

    def __insert(self):
        placeholders = ['%({})s'.format(
            field) for field in self.__fields.keys()
            ]

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
            col = '{0}_{1}=%s'.format(
                self.__table,
                self._get_column(column_name)
                )
            args.append(str(self._get_column(column_name)))
            columns.append(col)
        args.append(str(self.__id))
        query = self.__update_query.format(
            table=self.__table,
            columns=','.join(columns)
        )
        self.__execute_query(query, args)

    def full_name(self, column):
        return '{0}_{1}'.format(self.__table, column)

    def _get_column(self, name):
        self.__load()
        return self.__fields[self.full_name(name)]

    def _set_column(self, name, value):
        self.__fields[self.full_name(name)] = value
        self.__modified = True

    @classmethod
    def all(cls):        
        cursor = cls.db.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )
        query = cls.__list_query.format(table=cls.__name__.lower())
        cursor.execute(query) 
        
        for row in cursor.fetchall():
            instance = cls()
            instance.__fields = dict(row)
            instance.__loaded = True
            yield instance                 
            

    def delete(self):
        if self.__id is None:
            raise NotFoundError()
        query = self.__delete_query.format(
            table=self.__table
        )
        self.__execute_query(query, [self.__id])

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
    
    def _get_children(self, name):
        self.__load()
        entity_children = {cls.__name__: cls for cls in Entity.__subclasses__()}
        
        query = self.__class__.__parent_query.format(
        parent=self.__table,
        table=name.lower()
        )
        self.__execute_query(query, [self.__id])
        for row in self.__cursor.fetchall():
            instance = entity_children[name]
            instance.__fields = dict(row)
            instance.__loaded = True
            yield instance
        
        # return an array of child entity instances
        # each child instance must have an id and be filled with data
    
    def _get_parent(self, name):
        parrent_id = self.__fields['{0}_id'.format(name)]
        entity_children = {cls.__name__: cls for cls in Entity.__subclasses__()}
        instance = entity_children[name](parrent_id)
        instance.__load()
        return instance
        
        
        # ORM part 2
        # get parent id from fields with <name>_id as a key
        # return an instance of parent entity class with an appropriate id

    def _get_siblings(self, name):
        # ORM part 2
        # get parent id from fields with <name>_id as a key
        # return an array of sibling entity instances
        # each sibling instance must have an id and be filled with data
        pass

    def _set_parent(self, name, value):
        if hasattr(value, '__id'):
            value = value.__id
        self.__fields['{0}_id'.format(name)] = value
        # ORM part 2
        # put new value into fields array with <name>_id as a key
        # value can be a number or an instance of Entity subclass
        pass
