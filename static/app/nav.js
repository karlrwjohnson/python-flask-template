app.constant('LINKS', [
  { stateName: 'root',
    stateParams: {},
    text: 'Home'
  },
  { stateName: 'widgets',
    stateParams: {},
    text: 'Widgets'
  },
  { stateName: 'users',
    stateParams: {},
    text: 'Users'
  },
]);

app.directive('nav', function(LIB_ROOT, LINKS) {
  return {
    restrict: 'A',
    templateUrl: LIB_ROOT + 'nav.tpl.html',
    controller: function($scope) {
      $scope.links = LINKS;
    }
  }
});
