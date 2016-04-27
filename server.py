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


# Configure Flask
import app
app.init(__name__,
  static_folder='static',
  template_folder='templates'
)

import index
import widgets

if __name__ == '__main__':
  app.app.run(debug=True)


