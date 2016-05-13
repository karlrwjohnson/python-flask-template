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

  return {
    table: $resource('/table/:name', {name: '@name'}, methods)
  };
});
