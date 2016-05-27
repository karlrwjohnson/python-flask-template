app.directive('autoTable', function(LIB_ROOT) {

  return {
    restrict: 'E',
    scope: {
      'data': '=',
      'columns': '=?',
    },
    templateUrl: LIB_ROOT + 'directives/autoTable.tpl.html',
    controller: function($scope) {
      // Columns weren't specified: Generate columns based on data.
      if (!$scope.columns) {
        // Data might not have been populated yet: Use $watch() to wait for data.

        // Temporary value while we're waiting
        $scope.columns = [];
        var prevColumns = $scope.columns;
        var prevData = $scope.data;

        // Callback returned from $watch() that kills the listener
        var clearWatch;

        // Run this every time $scope.columns changes until it's valid
        function whileColumnsNotSet() {
          // Only act when the data has been filled in
          if ($scope.data.length > 0) {
            // Auto-generate columns if the user hasn't created them yet.
            if ($scope.columns.length === 0) {
              $scope.columns = Object.keys($scope.data[0])
                .map(function(columnName) {
                  return {key: columnName};
                });
            }
            clearWatch();
          }
        }

        // Set up the $watch expression
        clearWatch = $scope.$watch(/*$scope.columns*/ function() {
          return prevColumns === $scope.columns &&
                 prevData === $scope.data;
        }, whileColumnsNotSet);

        // Initial run
        whileColumnsNotSet();
      }
    }
  }
});
