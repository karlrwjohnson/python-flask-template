app.controller('TableCtrl', function(
  $localStorage,
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

  $scope.columnTableColumns = $scope.builtinColumnTableColumns.slice();

  $scope.tablePreviewRowLimit = {value: 20};

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

  $scope.tablePreviewRows = [];
  $scope.refreshTablePreview = function() {
    console.log($scope.tablePreviewRowLimit);
    resources.tableRows.query({
      name: table.name,
      limit: $scope.tablePreviewRowLimit.value,
    }).$promise.then(function(rows) {
      $scope.tablePreviewRows = rows;

      if (!('columnSettings' in $localStorage)) {
        $localStorage.columnSettings = {};
      }
      if (table.name in $localStorage.columnSettings) {
        $scope.tablePreviewColumns = $localStorage.columnSettings[table.name];
      } else {
        $scope.resetColumns();
      }
    });
  };
  $scope.resetColumns = function() {
    $scope.tablePreviewColumns =
    $localStorage.columnSettings[table.name] =
      Object.keys($scope.tablePreviewRows[0])
        .map(function(columnName) {
          return {key: columnName};
        });
  };
  $scope.refreshTablePreview();

});
