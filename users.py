import bcrypt
import flask

from   app import app
import database
import http_status
from   util import \
  auto_404, \
  json_response, \
  validate_post_data

class User (object):
  def __init__(self, id, username, name):
    self.id = id
    self.username = username
    self.name = name

def _get_user_password_hash(user_id):
  with database.cursor() as cursor:
    cursor.execute("select password_hash from users where id = %s", [user_id])
    row = auto_404(cursor.fetchone())
    return row[0] if row is not None else None

def _check_user_password(user_id, password):
  encoded_password = password.encode('utf-8') if type(password) == unicode else password
  existing_hash = _get_password_hash(user_id)
  return bcrypt.hashpw(encoded_password, existing_hash) == existing_hash

def _set_user_password(user_id, password):
  encoded_password = password.encode('utf-8') if type(password) == unicode else password
  new_hash = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
  with database.cursor() as cursor:
    cursor.execute("update users set password_hash = %s where id = %s",
      [new_hash, user_id])
    database.commit()

### Users

@app.route('/users', methods=['GET'])
@json_response
def get_users():
  with database.cursor() as cursor:
    cursor.execute("select id, username, name from users")
    return [
      User(id=row[0], username=row[1], name=row[2])
      for row in cursor
    ]

@app.route('/users/<int:id>', methods=['GET'])
@json_response
def get_user(user_id):
  with database.cursor() as cursor:
    cursor.execute("select id, username, name from users where id = %s", [user_id])
    row = auto_404(cursor.fetchone())
    return User(id=row[0], username=row[1], name=row[2])

@app.route('/users', methods=['POST'])
@validate_post_data({
  "username": str,
  "name": str,
  "password": str,
})
@json_response
def create_user():
  post_data = flask.request.get_json()
  with database.cursor() as cursor:
    cursor.execute("""
      insert into users (username, name)
      values (%s, %s)
      returning id, username, name
      """, [post_data['username'], post_data['name']])
    row = cursor.fetchone()
  _set_user_password(row[0], post_data['password'])
  return {'id': row[0], 'username': row[1], 'name': row[2]}

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
  with database.cursor() as cursor:
    cursor.execute("""
      delete from users
      where id = %s
      """, [user_id])
    database.commit()
    return flask.Response(status=http_status.NO_CONTENT)

### User Passwords

@app.route('/users/<int:id>/password', methods=['PUT'])
@validate_post_data({
  'old': str,
  'new': str
})
@json_response
def update_password(user_id):
  post_data = flask.request.get_json()
  if _check_user_password(user_id, post_data['old']):
    _set_user_password(user_id, post_data['new'])
    return NO_CONTENT_RESPONSE
  else:
    flask.error('Wrong password')
    flask.abort(http_status.FORBIDDEN)

@app.route('/users/<int:id>/password', methods=['POST'])
@validate_post_data(str)
@json_response
def set_password(user_id):
  _set_user_password(user_id, post_data)

