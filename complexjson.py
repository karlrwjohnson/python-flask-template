import json

class MyEncoder(json.JSONEncoder):
  """Encoder for json.dumps() which supports objects implementing a toJSON() method"""
  def default(self, thing):
    if hasattr(thing, 'toJSON') and callable(thing.toJSON):
      return thing.toJSON()
    else:
      return thing.__dict__

def dumps (thing):
  """Wrapper around json.dumps() which supports objects implementing a toJSON() method"""
  return json.dumps(thing, cls=MyEncoder)

