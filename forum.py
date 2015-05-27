import bottle
from beaker.middleware import SessionMiddleware

import settings
from db import database
from messageboard.models import *
from common.decorators import *

from users.routes import app as users_app
from messageboard.routes import app as forum_app

root = bottle.Bottle()
root.mount('/user', users_app)
root.mount('/board', forum_app)

session = SessionMiddleware(root, settings.SESSION_OPTS)

@root.route('/static/<filename:path>')
def serve_static(filename):
  return bottle.static_file(filename, root=settings.STATIC_ROOT)


@root.hook('before_request')
def before_request():
  database.connect()


@root.hook('after_request')
def after_request():
  database.close()


@root.route('/')
@bottle.view('index.html')
@append_request_context
def index():
  return {'categories': Category.select().where(Category.parent == None)}


# @app.post('/search')
# @bottle.view('search.html')
# @append_request_context
# def search():
#   query = bottle.request.forms.get('query')
#   return {
#     'query': query,
#     'results': {
#       'users': Profile.select().join(User).where(User.username**query),
#       'threads': Thread.select().where(Thread.title.contains(query)),
#       'categories': Category.select().where(Category.name.contains(query)),
#     }
#   }


if __name__ == '__main__':
  bottle.run(app=session, host='localhost', port=8080, debug=settings.DEBUG, reloader=True)
