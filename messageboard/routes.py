import bottle, peewee

from models import *
from common.decorators import *

app = bottle.Bottle()

all = ['app']


@app.route('/category/<cat_id:int>')
@bottle.view('category.html')
@append_request_context
@login_required
def category(cat_id):
  try:
    return {'category': Category.get(Category.id == cat_id)}
  except peewee.DoesNotExist:
    bottle.redirect('/')


@app.route('/thread/<thread_id:int>')
@bottle.view('thread.html')
@append_request_context
@login_required
def thread(thread_id):
  try:
    return {'thread': Thread.select().where(Thread.id == thread_id).join(Category).get()}
  except peewee.DoesNotExist:
    bottle.redirect('/')

