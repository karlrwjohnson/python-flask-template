import flask

from   app import app
import database
from   util import json_response, auto_404, NO_CONTENT_RESPONSE

class Widget (object):
  def __init__(self, id, name, data):
    self.id = id
    self.name = name
    self.data = data

  @staticmethod
  def fromJSON(obj):
    #validate(obj, {
    #  'id': either(notpresent, int),
    #  'name': str,
    #  'data': str
    #})
    #validate(obj, not_null=['name', 'data'])
    return Widget(
      id=obj['id'] if 'id' in obj else None,
      name=obj['name'],
      data=obj['data']
    )

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
@json_response
def post_widget():
  post_data = flask.request.get_json()
  if 'id' in post_data and post_data['id'] != None: 
    flask.error('POSTed object with a defined "id" attribute')
    abort(400)
  else:
    widget = Widget.fromJSON(post_data)
    with database.cursor() as cursor:
      cursor.execute("""
        insert into widgets (name, data)
        values (%s, %s)
        returning id, name, data
        """, [widget.name, widget.data])
      row = cursor.fetchone()
      database.commit()
      return Widget(id=row[0], name=row[1], data=row[2])

@app.route('/widgets/<int:id>', methods=['PUT'])
@json_response
def put_widget(id):
  post_data = flask.request.get_json()
  if 'id' in post_data and post_data['id'] == id: 
    widget = Widget.fromJSON(post_data)
    with database.cursor() as cursor:
      cursor.execute("""
        update widgets
        set name = %s, data = %s
        where id = %s
        returning id, name, data
        """, [widget.name, widget.data, widget.id])
      row = cursor.fetchone()
      database.commit()
      return Widget(id=row[0], name=row[1], data=row[2])
  else:
    flask.error('POSTed object lacks correct "id" attribute')
    abort(400)

@app.route('/widgets/<int:id>', methods=['DELETE'])
def delete_widget(id):
  with database.cursor() as cursor:
    cursor.execute("""
      delete from widgets
      where id = %s
      returning id, name, data
      """, [id])
    database.commit()
    return NO_CONTENT_RESPONSE

