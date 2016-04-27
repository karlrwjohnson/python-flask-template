import flask
import glob2
import yaml

from app import app

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

@app.route('/')
@app.route('/index.htm')
@app.route('/index.html')
def hello():
  rendered_homepage = flask.render_template('index.htm', scripts=scripts, stylesheets=stylesheets)
  return rendered_homepage


