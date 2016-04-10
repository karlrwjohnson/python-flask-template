app.service('resources', function($resource) {
  'use strict';

  var methods = {
    'get':    {method:'GET'},
    'query':  {method:'GET', isArray:true},
    'save':   {method:'POST'},
    'update': {method:'PUT'},
    'remove': {method:'DELETE'},
    'delete': {method:'DELETE'}
  };

  return {
    widgets: $resource('/widgets/:id', {id: '@id'}, methods),
  };
});
