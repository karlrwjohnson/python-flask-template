# Requirements (since I don't have virtualenv or a better dependency system
# set up yet)
# - Flask -- flask.pocoo.org
#    $ sudo pip install flask
# - psycopg2 -- initd.org/psycopg
#    $ sudo apt-get install libpq-dev python-dev  # Has to be built
#    $ sudo pip install psycopg2
# - PyYAML -- (references but doesn't require libyaml)
#    $ sudo pip install PyYAML
# - glob2 -- github.com/miracle2k/python-glob2

import contextlib
import flask
import glob2
import json
#import psycopg2
import pg8000 as psycopg2
import yaml

from complexjson import json_response
from model import *
#from validation import InvalidSerializationError



with open('env.yml') as envfile:
  env = yaml.load(envfile)

# Configure database connection
if env['POSTGRES_CONNECTION_TYPE'] == 'socket':
  dbconn = psycopg2.connect(
    database=env['POSTGRES_DATABASE'],
    user=env['POSTGRES_USER'],
    unix_sock='/var/run/postgresql/.s.PGSQL.5432'
  )
elif env['POSTGRES_CONNECTION_TYPE'] == 'network':
  dbconn = psycopg2.connect(
    database=env['POSTGRES_DATABASE'],
    user=env['POSTGRES_USER'],
    hostname=env['POSTGRES_HOSTNAME'],
    port=env['POSTGRES_PORT'] if 'POSTGRES_PORT' in env else 5432,
  )

def list_resources (globstrings):
  """Returns the resources matched by a list of globs, preventing duplicates
     from appearing later in the list."""
  ret = []
  found = set()
  for globstring in globstrings:
    for filename in glob2.glob(globstring):
      if filename not in found:
        ret.append(filename)
        found.add(filename)
  return ret

# Load external resource paths
with open('resources.yml') as resourcefile:
  resources = yaml.load(resourcefile)

scripts = list_resources(resources['scripts'])
stylesheets = list_resources(resources['stylesheets'])
#rendered_homepage = flask.render_template('index.htm', scripts=scripts, stylesheets=stylesheets)

# Configure application
app = flask.Flask(__name__,
  static_folder='static',
  template_folder='templates'
)

def auto_404(result):
  """Throw a 404 exception if a query returned no results"""
  if result == None:
    flask.abort(404)
  else:
    return result

NO_CONTENT_RESPONSE = ('', 204, {})

@app.route('/')
@app.route('/index.htm')
@app.route('/index.html')
def hello():
  rendered_homepage = flask.render_template('index.htm', scripts=scripts, stylesheets=stylesheets)
  return rendered_homepage

@app.route('/widgets', methods=['GET'])
@json_response
def get_widgets():
  with contextlib.closing(dbconn.cursor()) as cursor:
    cursor.execute("select id, name, data from widgets")
    return [
      Widget(id=row[0], name=row[1], data=row[2])
      for row in cursor
    ]

@app.route('/widgets/<int:id>', methods=['GET'])
@json_response
def get_widget(id):
  with contextlib.closing(dbconn.cursor()) as cursor:
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
    with contextlib.closing(dbconn.cursor()) as cursor:
      cursor.execute("""
        insert into widgets (name, data)
        values (%s, %s)
        returning id, name, data
        """, [widget.name, widget.data])
      row = cursor.fetchone()
      dbconn.commit()
      return Widget(id=row[0], name=row[1], data=row[2])

@app.route('/widgets/<int:id>', methods=['PUT'])
@json_response
def put_widget(id):
  post_data = flask.request.get_json()
  if 'id' in post_data and post_data['id'] == id: 
    widget = Widget.fromJSON(post_data)
    with contextlib.closing(dbconn.cursor()) as cursor:
      cursor.execute("""
        update widgets
        set name = %s, data = %s
        where id = %s
        returning id, name, data
        """, [widget.name, widget.data, widget.id])
      row = cursor.fetchone()
      dbconn.commit()
      return Widget(id=row[0], name=row[1], data=row[2])
  else:
    flask.error('POSTed object lacks correct "id" attribute')
    abort(400)

@app.route('/widgets/<int:id>', methods=['DELETE'])
def delete_widget(id):
  with contextlib.closing(dbconn.cursor()) as cursor:
    cursor.execute("""
      delete from widgets
      where id = %s
      returning id, name, data
      """, [id])
    dbconn.commit()
    return NO_CONTENT_RESPONSE

if __name__ == '__main__':
  app.run(debug=True)


