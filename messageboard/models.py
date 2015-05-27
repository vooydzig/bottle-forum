import peewee

from common.models import BaseModel
from users.models import Profile

__all__ = ['Category', 'Thread', 'Post']


class Category(BaseModel):
  name = peewee.CharField()
  description = peewee.TextField(null=True)
  parent = peewee.ForeignKeyField('self', null=True, related_name='children')


  def def_get_last_post_in_category(self):
    l = []
    for t in self.threads:
      p = t.get_newest_post()
      if p:
        l.append(p)
    if l:
      return sorted(l, key=lambda x: x.created, reverse=True)[0]
    return None


class Thread(BaseModel):
  category = peewee.ForeignKeyField(Category, related_name='threads')
  title = peewee.CharField()

  @staticmethod
  def get_posts_for_thread(id):
    try:
      t = Thread.get(Thread.id==id)
    except:
      return None
    return t.posts


  def get_newest_post(self):
    if self.posts.count():
      return self.posts\
        .select()\
        .join(Thread)\
        .order_by(-Post.created).get()


class Post(BaseModel):
  author = peewee.ForeignKeyField(Profile, related_name='posts')
  thread = peewee.ForeignKeyField(Thread, related_name='posts')

  body = peewee.TextField()
  is_sticky = peewee.BooleanField(default=False)
