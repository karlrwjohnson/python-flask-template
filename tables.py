import flask

from   app import app
import database
import http_status
import re
from   util import \
  auto_404, \
  cursor_column_names, \
  json_response, \
  validate_post_data

@app.route('/table', methods=['GET'])
@json_response
def get_tables():
  with database.cursor() as cursor:
    cursor.execute('''
        select table_name
        from information_schema.tables
        where table_schema = 'public'
          and table_type = 'BASE TABLE'
        order by table_name
    ''')
    return [
      row[0]
      for row in cursor
    ]

@app.route('/table/<table_name>', methods=['GET'])
@json_response
def get_table(table_name):
  print 'get_table called'
  return {
    'name': table_name,
    'columns': _get_table_columns(table_name),
    'foreignKeys': _get_table_foreign_keys(table_name),
    'foreignKeyReferences': _get_table_foreign_key_references(table_name),
  }


def _get_table_columns(table_name):
  with database.cursor() as cursor:
    # I have no idea what metadata I need, so this returns everything
    # the database can tell me about the columns. Last I checked, it
    # returned these fields:
    #  - table_catalog             - domain_catalog
    #  - table_schema              - domain_schema
    #  - table_name                - domain_name
    #  - column_name               - udt_catalog
    #  - ordinal_position          - udt_schema
    #  - column_default            - udt_name
    #  - is_nullable               - scope_catalog
    #  - data_type                 - scope_schema
    #  - character_maximum_length  - scope_name
    #  - character_octet_length    - maximum_cardinality
    #  - numeric_precision         - dtd_identifier
    #  - numeric_precision_radix   - is_self_referencing
    #  - numeric_scale             - is_identity
    #  - datetime_precision        - identity_generation
    #  - interval_type             - identity_start
    #  - interval_precision        - identity_increment
    #  - character_set_catalog     - identity_maximum
    #  - character_set_schema      - identity_minimum
    #  - character_set_name        - identity_cycle
    #  - collation_catalog         - is_generated
    #  - collation_schema          - generation_expression
    #  - collation_name            - is_updatable
    cursor.execute('''
      select *
      from information_schema.columns
      where table_name = %s
    ''', [table_name])
    column_names = cursor_column_names(cursor)
    return [
      dict(zip(column_names, row))
      for row in cursor
    ]

@app.route('/table/<table_name>/columns', methods=['GET'])
@json_response
def get_table_columns(table_name):
  return _get_table_columns(table_name)

# This is used in two different places for both parent and child FKs.
# This kind of thing is prone to copy-pasta errors.
FOREIGN_KEY_QUERY_STRING = '''
      select ref_cons.constraint_name   fkey_constraint,
             ref_cons.update_rule       update_rule,
             ref_cons.delete_rule       delete_rule,
             parent_tab_cons.table_name parent_table,
             child_tab_cons.table_name  child_table,
             to_json(array(
                     select json_build_object(
                              'parent', parent_key_col.column_name,
                              'child',  child_key_col.column_name
                            )
                       from information_schema.key_column_usage parent_key_col
                 inner join information_schema.key_column_usage child_key_col
                         on parent_key_col.ordinal_position = child_key_col.position_in_unique_constraint
                      where parent_key_col.constraint_name  = ref_cons.unique_constraint_name
                        and child_key_col.constraint_name   = ref_cons.constraint_name
             )) columns
        from information_schema.referential_constraints ref_cons
  inner join information_schema.table_constraints       parent_tab_cons
          on parent_tab_cons.constraint_name = ref_cons.unique_constraint_name
  inner join information_schema.table_constraints       child_tab_cons
          on child_tab_cons.constraint_name = ref_cons.constraint_name
'''

def _get_table_foreign_keys(table_name):
  with database.cursor() as cursor:
    cursor.execute(FOREIGN_KEY_QUERY_STRING + \
      'where parent_tab_cons.table_name = %s;', [table_name])
    column_names = cursor_column_names(cursor)
    return [
      dict(zip(column_names, row))
      for row in cursor
    ]

@app.route('/table/<table_name>/foreignkeys', methods=['GET'])
@json_response
def get_table_foreign_keys(table_name):
  return _get_table_foreign_keys(table_name)

def _get_table_foreign_key_references(table_name):
  with database.cursor() as cursor:
    cursor.execute(FOREIGN_KEY_QUERY_STRING + \
      'where child_tab_cons.table_name = %s;', [table_name])
    column_names = cursor_column_names(cursor)
    return [
      dict(zip(column_names, row))
      for row in cursor
    ]

@app.route('/table/<table_name>/foreignkeyreferences', methods=['GET'])
@json_response
def get_table_foreign_key_references(table_name):
  return _get_table_foreign_key_references(table_name)


@app.route('/table/<table_name>/rows', methods=['GET'])
@json_response
def get_table_rows(table_name):

  if not re.match(r'^[A-Za-z][A-Za-z0-9_]*$', table_name):
    print 'Invalid table name {}'.format(table_name)
    flask.abort(http_status.BAD_REQUEST)

  for arg in flask.request.args.keys():
    if not re.match(r'^[A-Za-z][A-Za-z0-9_]*$', table_name):
      print 'Invalid filter name {}'.format(arg)
      flask.abort(http_status.BAD_REQUEST)

  if 'limit' in flask.request.args:
    try:
      limit = int(flask.request.args['limit'])
    except ValueError:
      print 'Expected limit to be an integer; got {!r}'.format(flask.request.args['limit'])
      flask.abort(http_status.BAD_REQUEST)
  else:
    limit = 20

  # Extract dict to list to guarantee the keys are always iterated
  # in the same order
  filters = [ (k, v)
              for k, v in flask.request.args.iteritems()
              if k != 'limit' ]
  query_template = 'select * from {} '.format(table_name) + \
      ''.join([ 'where {} = %s '.format(key) for k, v in filters ]) + \
      'limit %s'
  query_template_parameters = tuple([v for k, v in filters] + [limit])

  print query_template
  print query_template_parameters
  print query_template % query_template_parameters

  with database.cursor() as cursor:
    cursor.execute(query_template, query_template_parameters);
    column_names = cursor_column_names(cursor)
    return [
      dict(zip(column_names, row))
      for row in cursor
    ]


#select to_json(ARRAY(
#    select json_build_object(
#        'data', f.data,
#        'comments', ARRAY(
#            select comment from bar b where b.foo_id = f.id
#        )
#    )
#    from foo f
#));


