app.controller('WidgetCtrl', function(
  $scope,
  $state,
  resources,
  widget
) {
  $scope.widget = widget;

  $scope.save = function() {
    if ('id' in $scope.widget) {
      $scope.widget.$update().then(function() {
        console.log('Updated successfully');
        $state.go('widgetsList');
      }, function(error) {
        console.error(error);
      });
    } else {
      resources.widgets.save($scope.widget, function() {
        console.log('Created successfully');
        $state.go('widgetsList');
      }, function(error) {
        console.error(error);
      });
    }
  }
});
