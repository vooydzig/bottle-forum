import os, peewee, bottle

import settings

from users.models import *
from common.decorators import *

app = bottle.Bottle()

all = ['app']


@app.get('/profile_id:int>')
@bottle.view('profile/view.html')
@append_request_context
@login_required
def view_profile(profile_id):
  try:
    return {'profile': Profile.select().where(Profile.id == profile_id).get()}
  except peewee.DoesNotExist:
    bottle.redirect('/')



@app.get('/edit/<profile_id:int>')
@bottle.view('profile/edit.html')
@append_request_context
@login_required
def profile(profile_id):
  try:
    return {'profile': Profile.select().where(Profile.id == profile_id).get()}
  except peewee.DoesNotExist:
    bottle.redirect('/')


@app.post('/edit/<profile_id:int>')
@bottle.view('profile/edit.html')
@append_request_context
@login_required
def edit_profile(profile_id):
  avatar = bottle.request.files.get('avatar')
  try:
    user = Profile.select().where(Profile.id == profile_id).get()
  except peewee.DoesNotExist:
    bottle.redirect('/')
  else:
    _, ext = os.path.splitext(avatar.filename)
    save_path = os.path.join(settings.STATIC_ROOT, 'avatars', 'user_%d' % user.id)
    avatar.save(save_path + ext)
    user.avatar = 'user_%d' % (user.id + ext)
    user.save()
    bottle.redirect('/user/%s' % user.id)

