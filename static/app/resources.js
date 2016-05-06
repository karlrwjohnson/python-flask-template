app.service('resources', function($resource) {
  'use strict';

  // Standard HTTP methods on an object
  var methods = {
    'get':    {method:'GET'},
    'query':  {method:'GET', isArray:true},
    'save':   {method:'POST'},
    'update': {method:'PUT'},     // This one is not defined out-of-the-box
    'remove': {method:'DELETE'},
    'delete': {method:'DELETE'}
  };

  /**
   * Add a .new() method to a resource object which returns a template object
   * @param {Resource} resource - object to modify
   * @param {Object} template - object to duplicate and return when .new() is called
   * @return {Resource} - The original resource object
   */
  function addTemplate(resource, template) {
    resource.new = function() {
      return angular.copy(template);
    }
    return resource;
  }

  return {
    widgets: addTemplate(
      $resource('/widgets/:id', {id: '@id'}, methods),
      { name: '', data: '' }
    ),
    users: addTemplate(
      $resource('/users/:id', {id: '@id'}, {
        'get': methods.get,
        'query': methods.query,
        'delete': methods.delete,
        'save': methods.save,
      }),
      { username: '', name: '' }
    ),
  };
});
