app.controller('TableCtrl', function(
  $scope,
  $state,
  resources,
  table,
  tables
) {
  $scope.table = table;
  $scope.tables = tables;

  $scope.builtinColumnTableColumns = [
    {label: 'Column', key: 'column_name'},
    {label: 'Nullable', formula: function(column) {return column.is_nullable === 'YES';}},
    {label: 'Data Type', formula: function(column) {
      return column.data_type + 
             (column.character_maximum_length !== null ? '(' + column.character_maximum_length + ')' : '');
    }},
    {label: 'Default', key: 'column_default'},
  ];

  $scope.columnTableColumns = $scope.builtinColumnTableColumns.slice()

  $scope.table.$promise.then(function() {
    if ($scope.table.columns.length > 0) {
      var allColumns = Object.keys($scope.table.columns[0])
        .sort()
        .map(function(columnName) {
          return { label: columnName, key: columnName, disabled: true };
        });
      [].push.apply($scope.columnTableColumns, allColumns);
    }
  });

  $scope.showAll = function() {
    for (var i = 0; i < $scope.columnTableColumns.length; i++) {
      $scope.columnTableColumns[i].disabled = false;
    }
  };

  $scope.showDefaults = function() {
    for (var i = 0; i < $scope.columnTableColumns.length; i++) {
      $scope.columnTableColumns[i].disabled = (i >= $scope.builtinColumnTableColumns.length);
    }
  };

});
