app.controller('WidgetListCtrl', function(
  $scope,
  $state,
  highlight,
  widgets
) {
  $scope.widgets = widgets;
  $scope.highlight = highlight;

  console.log('highlight = ', highlight);

  $scope.delete = function(widget) {
    widget.$delete().then(function() {
      // Force reload regardless of params changing
      $state.reload(true);
    }, function(error) {
      console.error(error);
    });
  };
});
