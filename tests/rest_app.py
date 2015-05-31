import unittest, peewee, webtest, datetime, bottle
from playhouse.test_utils import test_database

from rest import RestApp, AbstractRestApp
from common.models import BaseModel

test_db = peewee.SqliteDatabase(':memory:')

__all__= ['RestApiAppTests',
          'RestApiAppGETListTests',
          'RestApiAppGETItemTests'
]

class SubModel(BaseModel):
  int_field = peewee.IntegerField(default=100)

class Model(BaseModel):
  unique_field = peewee.IntegerField(default=1, unique=True)
  int_field = peewee.IntegerField(default=1)
  dt_field = peewee.DateTimeField(default=datetime.datetime.now())
  str_field = peewee.TextField(default='test')
  fk_field = peewee.ForeignKeyField(SubModel)


class RestApiAppTests(unittest.TestCase):
  class InvalidModel(peewee.BaseModel):
    int_field = peewee.IntegerField(default=1)

  class InvalidModel2(peewee.BaseModel):
    int_field = peewee.IntegerField(default=1)

    def to_dict(self):
      pass


  def test_init_with_invald_model_raises_error(self):
    with self.assertRaises(bottle.BottleException):
      RestApp(RestApiAppTests.InvalidModel, '/test')

    with self.assertRaises(bottle.BottleException):
      RestApp(RestApiAppTests.InvalidModel2, '/test')

  def test_REST_methods_return_404_by_default(self):
    app = webtest.TestApp(AbstractRestApp(Model, '/test'))
    self.assertEqual(app.get('/test/', expect_errors=True).status_int, 404)
    self.assertEqual(app.post('/test/', expect_errors=True).status_int, 404)
    self.assertEqual(app.get('/test/1/', expect_errors=True).status_int, 404)
    self.assertEqual(app.put('/test/1/', expect_errors=True).status_int, 404)
    self.assertEqual(app.delete('/test/1/', expect_errors=True).status_int, 404)


  def test_REST_methods_return_405_when_not_implemented(self):
    app = webtest.TestApp(AbstractRestApp(Model, '/test'))
    self.assertEqual(app.put('/test/', expect_errors=True).status_int, 405)
    self.assertEqual(app.delete('/test/', expect_errors=True).status_int, 405)
    self.assertEqual(app.post('/test/1/', expect_errors=True).status_int, 405)


class RestApiAppGETListTests(unittest.TestCase):
  def setUp(self):
    self.app = webtest.TestApp(RestApp(Model, '/test', catchall=False))


  def test_list_returns_model_list(self):
    with test_database(test_db, [Model, SubModel], create_tables=True):
      s = SubModel.create()
      for i in xrange(25):
        Model.create(fk_field=s, unique_field=i)
      data = self.app.get('/test/').json
      self.assertEqual(len(data['items']), 20)


  def test_list_paginates_by_20_by_default(self):
    with test_database(test_db, [Model, SubModel], create_tables=True):
      s = SubModel.create()
      for i in xrange(25):
        Model.create(fk_field=s, unique_field=i)
      data = self.app.get('/test/').json
      self.assertEqual(data['page'], 1)
      self.assertEqual(data['count'], 20)


  def test_list_returns_exact_amount_of_items(self):
    with test_database(test_db, [Model, SubModel], create_tables=True):
      s = SubModel.create()
      for i in xrange(5):
        Model.create(fk_field=s, unique_field=i)
      data = self.app.get('/test/').json
      self.assertEqual(len(data['items']), 5)
      self.assertEqual(data['page'], 1)
      self.assertEqual(data['count'], 5)


  def test_list_paginates_by_specified_amount(self):
    with test_database(test_db, [Model, SubModel], create_tables=True):
      s = SubModel.create()
      for i in xrange(20):
        Model.create(fk_field=s, unique_field=i)

      for i in range(4):
        data = self.app.get('/test/', {'page': i, 'count': 5}).json
        self.assertEqual(len(data['items']), 5)
        self.assertEqual(data['page'], i)
        self.assertEqual(data['count'], 5)


class RestApiAppGETItemTests(unittest.TestCase):
  def setUp(self):
    self.app = webtest.TestApp(RestApp(Model, '/test'))


  def test_GET_returns_item_with_specified_id(self):
    with test_database(test_db, [SubModel, Model], create_tables=True):
      s = SubModel.create()
      for i in xrange(15):
        Model.create(fk_field=s, unique_field=i)
      for i in xrange(1, 15):
        data = self.app.get('/test/'+str(i)+'/').json
        self.assertEqual(data['id'], i)


  def test_if_item_does_not_exist_error_is_returned(self):
    with test_database(test_db, [Model, SubModel], create_tables=True):
      s = SubModel.create()
      for i in xrange(20):
        Model.create(fk_field=s, unique_field=i)

      data = self.app.get('/test/100/').json
      self.assertIsNone(data.get('id'))
      self.assertIsNotNone(data.get('error'))


  def test_POST_creates_if_item_does_not_exist(self):
    now = datetime.datetime.now()
    with test_database(test_db, [Model, SubModel], create_tables=True):
      s = SubModel.create()
      data = self.app.post('/test/', {
        'int_field': 10,
        'dt_field': now,
        'str_field': 'Test User',
        'fk_field': s.id
      }).json
      self.assertEqual(data['id'], 1)
      self.assertEqual(data['uri'], '/test/1/')

      created = Model.select().join(SubModel).where(Model.id == 1).get()
      self.assertEqual(created.int_field, 10)
      self.assertEqual(created.dt_field, now)
      self.assertEqual(created.str_field, 'Test User')
      self.assertEqual(created.fk_field.int_field, 100)

      data = self.app.get(data['uri']).json
      self.assertEqual(data['id'], 1)


  def test_POST_does_not_create_if_item_exists(self):
    with test_database(test_db, [SubModel, Model], create_tables=True):
      s = SubModel.create()
      Model.create(unique_field=100, fk_field=s)
      data = self.app.post('/test/', {
        'unique_field': 100,
        'fk_field': s.id
      }).json
      self.assertIsNone(data.get('id'))
      self.assertIsNotNone(data.get('error'))


  def test_PUT_updates_user_by_id(self):
    with test_database(test_db, [SubModel, Model], create_tables=True):
      s = SubModel.create()
      Model.create(fk_field=s, int_field = 10)
      data = self.app.put('/test/1/', {
        'int_field': 100
      }).json

      self.assertEqual(data['id'], 1)
      self.assertEqual(data['uri'], '/test/1/')
      data = self.app.get(data['uri']).json
      self.assertEqual(data['int_field'], 100)


  def test_PUT_does_not_update_not_existing_item(self):
    with test_database(test_db, [SubModel, Model], create_tables=True):
      data = self.app.put('/test/100/', {
        'int_field': 100
      }).json

      self.assertIsNone(data.get('id'))
      self.assertIsNotNone(data.get('error'))


  def test_DELETE_removes_an_item(self):
    with test_database(test_db, [SubModel, Model], create_tables=True):
      s = SubModel.create()
      Model.create(fk_field=s)
      data = self.app.delete('/test/1/').json
      self.assertTrue(data['deleted'])

  def test_DELETE_does_not_remove_if_id_is_invalid(self):
    with test_database(test_db, [SubModel, Model], create_tables=True):
      s = SubModel.create()
      Model.create(fk_field=s)
      data = self.app.delete('/test/100/').json
      self.assertIsNone(data.get('deleted'))
      self.assertIsNotNone(data.get('error'))