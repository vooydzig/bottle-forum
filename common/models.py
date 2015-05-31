import datetime, peewee, json, calendar
from playhouse import shortcuts


from db import database

class BaseModel(peewee.Model):
  created = peewee.DateTimeField(default=datetime.datetime.now)
  updated = peewee.DateTimeField(default=datetime.datetime.now)

  class Meta:
    database = database


  def to_dict(self):
    data = shortcuts.model_to_dict(self)
    for name in data:
      value = data[name]
      if isinstance(value, datetime.datetime):
        data[name] = calendar.timegm(value.timetuple())
      if isinstance(value, dict):
        data[name] = value.get('id')
      if isinstance(value, list):
        data[name + '_count'] = len(value)
    return data


  @classmethod
  def from_dict(cls, data):
    model = shortcuts.dict_to_model(cls, data)
    return model