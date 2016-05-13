app.directive('pulldown', function(LIB_ROOT) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      'buttonClass': '@?',
      'buttonText': '@',
      'width': '@?',
      'height': '@?',
      'anchor': '@?',
      'paneStyle': '@?',
    },
    templateUrl: LIB_ROOT + 'directives/pulldown.tpl.html',
    controller: function($scope) {
      if (!$scope.buttonClass) {
        $scope.buttonClass = 'btn btn-default';
      }
      $scope.expanded = false;

      if ($scope.anchor) {
        if ($scope.anchor !== 'left' && $scope.anchor !== 'right') {
          throw Error('Expected anchor property to be "left" or "right"');
        }
      } else {
        $scope.anchor = 'left';
      }

      $scope.toggle = function() {
        $scope.expanded = !$scope.expanded;
      }
    }
  }
});
