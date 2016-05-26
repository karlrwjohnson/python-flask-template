app.factory('TableListService', function(resources) {
  var ret = {};
  Object.defineProperties(ret, {
    '_tables': { writable: true, enumerable: false, value: null },
    'tables': { get: function() {
      if (!this._tables) {
        this.refresh();
      }
      return this._tables;
    }},
    'refresh': { value: function() {
      this._tables = resources.table.query().$promise;
      return this._tables;
    }},
  });
  return ret;
});
