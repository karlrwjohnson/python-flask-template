import functools

_javascript_type_name = {
  list: 'array',
  dict: 'object',
  type(None): 'null',
  int: 'integer',
  float: 'number',
  str: 'string',
  unicode: 'string'
}

def validate (spec, data, path=''):
  # Any-of-type
  if type(spec) is type:
    if type(data) is spec \
        or (type(data) is int and spec is float) \
        or (type(data) is unicode and spec is str):
      return []
    else:
      return ['Item {} must be a {}, but is a(n) {} (got {!r})'.format(
        path,
        _javascript_type_name[spec],
        _javascript_type_name[type(data)],
        data
      )]

  # Exact object
  elif type(spec) is dict:
    if type(data) is dict:
      return _validate_dict_exact(spec, data)
    else:
      return ['Item {} must be an object'.format(path)]

  # Array-of-type
  elif type(spec) is list:
    if len(spec) == 0:
      assert False, '''
        Found an empty list in a specification, which is illegal. To validate
        that something is a list of arbitrary objects, say "list". To validate
        that items conform to a schema, pass a list containing a specification
        for those items.'''

    assert len(spec) == 1, \
      'List specification must contain only one validation item; found %' % len(spec)

    if type(data) is list:
      return _validate_list_of(spec[0], data)
    else:
      return ['Item {} must be an array'.format(path)]

  # Custom validation
  elif callable(spec):
    return spec(data)

  # Literal
  else:
    if data == spec:
      return []
    else:
      return ['Item {} must equal {!r}, but is {!r}'.format(path, spec, data)]

def AND(*specs):
  def _AND(data, path=''):
    return [error
      for spec in specs
      for error in validate(spec, data, path)
    ]
  return _AND

def OR(*specs):
  def _OR(data, path=''):
    return [{
      'message': 'Item {} did not fit any of the following specifications:'.format(path),
      'errors': [
        validate(spec, data, path)
        for spec in specs
      ]
    }]
  return _OR

def DICT_CONTAINING(spec):
  return functools.partial(_validate_dict_contains, spec)

def _validate_dict_contains(spec, data, path=''):
  errors = []

  for spec_key, spec_value in spec.iteritems():
    key_path = '{}.{}'.format(path, spec_key)
    if spec_key not in data:
      errors += 'Missing required key {}'.format(key_path)
    else:
      errors.extend(validate(spec_value, data[spec_key], path=key_path))

  return errors

def _validate_dict_exact(spec, data, path=''):
  errors = _validate_dict_contains(spec, data, path);

  for data_key in data.keys():
    if data_key not in spec:
      errors += 'Illegal key {}.{}'.format(path, data_key)

  return errors

def _validate_list_of(spec, data, path=''):
  errors = []
  for i in range(len(data)):
    item_path = '{}[{}]'.format(path, i)
    errors.extend(validate(spec, data[i], item_path))
  return errors


