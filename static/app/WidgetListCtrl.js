app.controller('WidgetListCtrl', function(
  $scope,
  $state,
  widgets
) {
  $scope.widgets = widgets;

  $scope.delete = function(widget) {
    widget.$delete().then(function() {
      // Force reload regardless of params changing
      $state.reload(true);
    }, function(error) {
      console.error(error);
    });
  };
});
