import urllib, hashlib
import peewee

from common import models

__all__ = ['Profile', 'Role']

class Role(models.BaseModel):
  name = peewee.CharField()
  level = peewee.IntegerField()


class Profile(models.BaseModel):
  role = peewee.ForeignKeyField(Role)

  username = peewee.CharField(null=False)
  email = peewee.CharField(null=False, unique=True)

  avatar = peewee.CharField(null=True)
  description = peewee.CharField(null=True)
  uses_gravatar = peewee.BooleanField(default=False)
  location = peewee.CharField(null=True)
  title = peewee.CharField(null=True)


  def get_avatar(self,size=64):
    if self.uses_gravatar:
      return self.get_gravatar(size)
    if self.avatar:
      return '/static/avatars/'+self.avatar
    return 'http://www.gravatar.com/avatar/00000000000000000000000000000000?d=mm&f=y&s='+str(size)


  def get_gravatar(self, size):
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':'mm', 's':str(size)})

