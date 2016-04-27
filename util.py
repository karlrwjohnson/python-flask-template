import flask

from complexjson import dumps

def json_response (fn):
  """Decorator for Flask view functions that encodes responses to JSON."""
  def json_response_wrapper(*args, **kwargs):
    return dumps(fn(*args, **kwargs))

  # Mirror the __name__ so Flask doesn't get confused
  json_response_wrapper.__name__ = fn.__name__

  return json_response_wrapper

def auto_404(result):
  """Throw a 404 exception if a query returned no results"""
  if result == None:
    flask.abort(404)
  else:
    return result

# An object to reply from a Flask route function corresponding to HTTP 204 No Content
NO_CONTENT_RESPONSE = ('', 204, {})

