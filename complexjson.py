import json

class MyEncoder(json.JSONEncoder):
  def default(self, thing):
    if hasattr(thing, 'toJSON') and callable(thing.toJSON):
      return thing.toJSON()
    else:
      return thing.__dict__

def dumps (thing):
  return json.dumps(thing, cls=MyEncoder)

def json_response (fn):
  """Just a decorator that encodes everything to JSON.
     Used on Flask view functions
  """
  def json_response_wrapper(*args, **kwargs):
    return dumps(fn(*args, **kwargs))

  # Mirror the __name__ so Flask doesn't get confused
  json_response_wrapper.__name__ = fn.__name__

  return json_response_wrapper 
