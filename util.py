import flask

from   complexjson import dumps
import http_status
import validation

def json_response (fn):
  """Decorator for Flask view functions that encodes responses to JSON."""
  def _json_response(*args, **kwargs):
    return flask.Response(
      status=http_status.OK,
      headers={'Content-type': 'text/json'},
      response=dumps(fn(*args, **kwargs))
    )

  # Mirror the __name__ so Flask doesn't get confused
  _json_response.__name__ = fn.__name__

  return _json_response

def validate_post_data (spec):
  def _validate_post_data_fn (endpoint_fn):
    def _validate_post_data_on_operation (*args, **kwargs):
      validation_errors = validation.validate(spec, flask.request.get_json())
      print validation_errors
      if len(validation_errors):
        return flask.Response(
          status=http_status.BAD_REQUEST,
          headers={'Content-type: text/json'},
          response=dumps({
            'errors': validation_errors
          })
        )
      else:
        return endpoint_fn(*args, **kwargs)
        

    # Mirror the __name__ so Flask doesn't get confused
    _validate_post_data_on_operation.__name__ = endpoint_fn.__name__

    return _validate_post_data_on_operation
  return _validate_post_data_fn


def auto_404(result):
  """Throw a 404 exception if a query returned no results"""
  if result == None:
    flask.abort(http_status.NOT_FOUND)
  else:
    return result

def cursor_column_names(cursor):
  '''Extract the names of the columns returned by the last query'''
  return [column_description[0] for column_description in cursor.description]




