from entity import *
import psycopg2.extras

class Section(Entity):
    _columns  = ['title']
    _parents  = []
    _children = {'categories': 'Category'}
    _siblings = {}

class Category(Entity):
    _columns  = ['title']
    _parents  = ['section']
    _children = {'posts': 'Post'}
    _siblings = {}

class Post(Entity):
    _columns  = ['content', 'title']
    _parents  = ['category']
    _children = {'comments': 'Comment'}
    _siblings = {'tags': 'Tag'}

class Comment(Entity):
    _columns  = ['text']
    _parents  = ['post', 'user']
    _children = {}
    _siblings = {}

class Tag(Entity):
    _columns  = ['name']
    _parents  = []
    _children = {}
    _siblings = {'posts': 'Post'}

class User(Entity):
    _columns  = ['name', 'email', 'age']
    _parents  = []
    _children = {'comments': 'Comment'}
    _siblings = {}


if __name__ == "__main__":
    connect = psycopg2.connect('dbname=test_database user=test_user')
    cursor = connect.cursor(
        cursor_factory=psycopg2.extras.DictCursor
    )
    cursor.execute('select * from article where article_id = 1;')

    section = Section()
    section.title = "zalupa"
    section.save()

#    for section in Section.all():
 #       print (section.title)
