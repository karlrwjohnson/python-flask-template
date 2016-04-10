

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
