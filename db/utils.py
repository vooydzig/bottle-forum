import json

from users.models import Profile, Role
from messageboard.models import Category, Thread, Post

from db import database
import settings


def create_tables():
  database.connect()
  Category.drop_table(fail_silently=True)
  Thread.drop_table(fail_silently=True)
  Post.drop_table(fail_silently=True)
  Role.drop_table(fail_silently=True)
  Profile.drop_table(fail_silently=True)
  database.create_tables([Category, Thread, Post, Profile, Role])
  database.close()

  if settings.DEBUG:
    setup_temp_data()


def create_temp_categories():
  with open('fixtures/categories.json') as f:
    cats = json.load(f)
    for c in cats:
      Category.create(name=c['name'], description=c['description'], parent=c['parent'])


def create_temp_roles():
  Role.create(name='admin', level=100)
  Role.create(name='moderator', level=50)
  Role.create(name='user', level=1)


def create_temp_users():
  _create_user('admin', 'admin')

  _create_user('mod1', 'moderator')
  _create_user('mod2', 'moderator')
  _create_user('mod3', 'moderator')

  with open('fixtures/profiles.json') as f:
    profiles = json.load(f)
    for row in profiles:
      _create_user('user' + str(row['id']), 'user', row)


def _create_user(username, rolename, data=None):
  if data is None:
    data = {}
  role = Role.select().where(Role.name==rolename).get()
  Profile.create(username=username, email=username+'@srv.pl', role=role,
                 description=data.get('description', 'User ' + username + ' description'),
                 title=data.get('title', 'User ' + username + ' title'),
                 location=data.get('location', 'User ' + username + ' location'))



def create_temp_threads():
  with open('fixtures/threads.json') as f:
    threads = json.load(f)
    for t in threads:
      c = Category.select().where(Category.id==t['category']).get()
      Thread.create(category=c, title=t['title'])


def create_temp_posts():
  with open('fixtures/posts.json') as f:
    posts = json.load(f)
    for p in posts:
      t = Thread.select().where(Thread.id==p['thread']).get()
      u = Profile.select().where(Profile.id==p['author']).get()
      Post.create(author=u, thread=t, body=p['body'], is_sticky=[['is_sticky']])


def setup_temp_data():
  with database.transaction():
    create_temp_roles()
    create_temp_users()
    create_temp_categories()
    create_temp_threads()
    create_temp_posts()

if __name__=='__main__':
  create_tables()