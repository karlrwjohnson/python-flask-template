import flask

from   app import app
import database
import http_status
from   util import \
  auto_404, \
  json_response, \
  validate_post_data

class Widget (object):
  def __init__(self, id, name, data):
    self.id = id
    self.name = name
    self.data = data

@app.route('/widgets', methods=['GET'])
@json_response
def get_widgets():
  with database.cursor() as cursor:
    cursor.execute("select id, name, data from widgets")
    return [
      Widget(id=row[0], name=row[1], data=row[2])
      for row in cursor
    ]

@app.route('/widgets/<int:id>', methods=['GET'])
@json_response
def get_widget(id):
  with database.cursor() as cursor:
    cursor.execute("select id, name, data from widgets where id = %s", [id])
    row = auto_404(cursor.fetchone())
    return Widget(id=row[0], name=row[1], data=row[2])


@app.route('/widgets', methods=['POST'])
@validate_post_data({
  'name': str,
  'data': str
})
@json_response
def post_widget():
  post_data = flask.request.get_json()
  with database.cursor() as cursor:
    cursor.execute("""
      insert into widgets (name, data)
      values (%s, %s)
      returning id, name, data
      """, [post_data['name'], post_data['data']])
    row = cursor.fetchone()
    database.commit()
    return Widget(id=row[0], name=row[1], data=row[2])

@app.route('/widgets/<int:id>', methods=['PUT'])
@validate_post_data({
  'id': int,
  'name': str,
  'data': str
})
@json_response
def put_widget(id):
  post_data = flask.request.get_json()
  with database.cursor() as cursor:
    cursor.execute("""
      update widgets
      set name = %s, data = %s
      where id = %s
      returning id, name, data
      """, [post_data['name'], post_data['data'], post_data['id']])
    row = cursor.fetchone()
    database.commit()
    return Widget(id=row[0], name=row[1], data=row[2])

@app.route('/widgets/<int:id>', methods=['DELETE'])
def delete_widget(id):
  with database.cursor() as cursor:
    cursor.execute("""
      delete from widgets
      where id = %s
      """, [id])
    database.commit()
    return flask.Response(status=http_status.NO_CONTENT)

