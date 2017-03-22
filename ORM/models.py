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
    Entity.db = psycopg2.connect('dbname=test_db user=postgres password=admin')
    # sect = Section()
    # sect.title = 'zalupa'
    # sect.save()
    # sect = Section()
    # sect.title = 'zal'
    # sect.save()
    # for section in Section.all():
    #     print(section.title)
    # categ = Category()
    # categ.title = 'zalupa'
    # categ._set_parent('section', 1)
    # categ.save()

    # post = Post()
    # post.content = 'ololo'
    # post.text = 'trololo'
    # post._set_parent('category', 4)
    # post.save()
    
    category = Category(4)
    for child in category._get_children('Post'):
        print (child.title)
    
