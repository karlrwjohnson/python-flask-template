from   contextlib import closing
#import psycopg2
import pg8000 as psycopg2

from env import env

_dbconn = None

def get ():
  global _dbconn

  if  _dbconn is None:
    # Configure database connection
    if env['POSTGRES_CONNECTION_TYPE'] == 'socket':
      _dbconn = psycopg2.connect(
      database=env['POSTGRES_DATABASE'],
      user=env['POSTGRES_USER'],
      unix_sock='/var/run/postgresql/.s.PGSQL.5432'
      )
    elif env['POSTGRES_CONNECTION_TYPE'] == 'network':
      _dbconn = psycopg2.connect(
      database=env['POSTGRES_DATABASE'],
      user=env['POSTGRES_USER'],
      hostname=env['POSTGRES_HOSTNAME'],
      port=env['POSTGRES_PORT'] if 'POSTGRES_PORT' in env else 5432,
      )
    else:
      raise RuntimeError('Unknown conneciton type {}'.format(env['POSTGRES_CONNECTION_TYPE']))

  return _dbconn

def cursor():
  return closing(get().cursor())

def commit():
  get().commit()

