from users import models


def get_breadcrumbs_for_category(id):
  try:
    category = models.Category.get(models.Category.id == id)
    return {'category': {'id': category.id, 'name': category.name}}
  except:
    return {}


def get_breadcrumbs_for_thread(id):
  try:
    thread = models.Thread.select().where(models.Thread.id == id).join(models.Category).get()
    return {'thread': {'id': thread.id, 'name': thread.title}}\
      .update(get_breadcrumbs_for_category(thread.category.id))
  except:
    return {}


def get_breadcrumbs(category_id, thread_id):
  print category_id, thread_id
  if category_id is None and thread_id is None:
    return {}

  if category_id:
    return get_breadcrumbs_for_category(category_id)

  return get_breadcrumbs_for_thread(thread_id)


def breadcrumbs(category_id=None, thread_id=None):
  def wrap(f):
    def wrapped(*args, **kwrds):
      response = f(*args, **kwrds)
      response['navigation'] = get_breadcrumbs(category_id, thread_id)
      print response
      return response
    return wrapped
  return wrap
