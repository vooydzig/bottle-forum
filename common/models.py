import datetime
import peewee

from db import database

class BaseModel(peewee.Model):
  created = peewee.DateTimeField(default=datetime.datetime.now)
  updated = peewee.DateTimeField(default=datetime.datetime.now)

  class Meta:
    database = database

