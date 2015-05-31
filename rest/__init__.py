import bottle, peewee

all = ['RestApp']

class AbstractRestApp(bottle.Bottle):
  def __init__(self, model, urlbase, catchall=True, autojson=True):
    if not 'to_dict' in dir(model):
      raise bottle.BottleException('Model must implement `to_dict` method')

    if not 'from_dict' in dir(model):
      raise bottle.BottleException('Model must implement `from_dict` method')

    super(AbstractRestApp, self).__init__(catchall, autojson)
    self.model = model
    self.urlbase = urlbase

    self.setup_routing()


  @staticmethod
  def get_records_range(data):
    return int(data.get('page', 1)), int(data.get('count', 20))


  def setup_routing(self):
    self.route(self.urlbase + '/', 'GET', self.get_list)
    self.route(self.urlbase + '/', 'POST', self.create_one)
    self.route(self.urlbase + '/<id>/', 'GET', self.get_one)
    self.route(self.urlbase + '/<id>/', 'PUT', self.update_one)
    self.route(self.urlbase + '/<id>/', 'DELETE', self.delete_one)


  def get_list(self):
    bottle.abort(404)

  def create_one(self):
    bottle.abort(404)

  def get_one(self, id):
    bottle.abort(404)

  def update_one(self, id):
    bottle.abort(404)

  def delete_one(self, id):
    bottle.abort(404)


class RestApp(AbstractRestApp):

  def get_list(self):
    p, c = self.get_records_range(bottle.request.query)
    profiles = self.model.select().order_by(self.model.id).paginate(p, c)
    return { 'page': p, 'count': profiles.count(),
             'items': [profile.to_dict() for profile in profiles]}


  def create_one(self):
    m = self.model.from_dict(bottle.request.forms)
    try:
      m.save()
    except Exception as e:
      return {'error': 'Error creating item: %s' % unicode(e)}
    return {'id': m.id, 'uri': '%s/%d/' %(self.urlbase, m.id)}


  def get_one(self, id):
    try:
      return self.model.select().where(self.model.id==id).get().to_dict()
    except peewee.DoesNotExist:
      return {'error': 'Item does not exist'}


  def update_one(self, id):
    q = self.model.update(**bottle.request.forms).where(self.model.id==id)
    if q.execute() != 1:
      return {'error': 'Item does not exist'}
    m = self.model.select().where(self.model.id==id).get()
    return {'id': m.id, 'uri': '%s/%d/' %(self.urlbase, m.id)}


  def delete_one(self, id):
    if self.model.delete().where(self.model.id==id).execute() != 1:
      return {'error': 'Item does not exist'}
    return {'deleted': True}