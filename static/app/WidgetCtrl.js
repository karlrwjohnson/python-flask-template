app.controller('WidgetCtrl', function(
  $scope,
  $state,
  resources,
  widget
) {
  $scope.widget = widget;

  $scope.save = function() {
    if ('id' in $scope.widget) {
      $scope.widget.$update().then(function(widget) {
        console.log('Updated successfully');
        $state.go('widgets.list', {highlight: widget.id});
      }, function(error) {
        console.error(error);
      });
    } else {
      resources.widgets.save($scope.widget, function() {
        console.log('Created successfully');
        $state.go('widgets.list', {highlight: widget.id});
      }, function(error) {
        console.error(error);
      });
    }
  }
});
