import bottle

import settings

__all__ = ['append_request_context', 'login_required', 'not_logged_in_required']

def _session():
  return bottle.request.environ.get('beaker.session')

def _get_request_context():
  return bottle.FormsDict({
    'app_name': settings.APP_NAME
  })

def append_request_context(func):
  def wrapper(*args, **kwargs):
    response = func(*args, **kwargs)
    if response is None:
      response = {}
    response['session'] = _session()
    response['context'] = _get_request_context()
    return response
  return wrapper


def login_required(func):
  def wrapper(*args, **kwargs):
    # if _session().get('user'):
    return func(*args, **kwargs)
    # bottle.redirect('/login?next=' + bottle.request.path)
  return wrapper


def not_logged_in_required(func):
  def wrapper(*args, **kwargs):
    if _session().get('user'):
      raise bottle.HTTPError(body='User already logged in')
    return func(*args, **kwargs)
  return wrapper

