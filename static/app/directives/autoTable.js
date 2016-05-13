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

        // Callback returned from $watch() that kills the listener
        var clearWatch;

        // Run this every time $scope.columns changes until it's valid
        function whileColumnsNotSet() {
          if ($scope.data.length > 0) {
            $scope.columns = Object.keys($scope.data[0])
              .map(function(columnName) {
                return {name: columnName};
              });
            clearWatch();
          }
        }

        // Set up the $watch expression
        clearWatch = $scope.$watch($scope.columns, whileColumnsNotSet);

        // Initial run
        whileColumnsNotSet();
      }
    }
  }
});
