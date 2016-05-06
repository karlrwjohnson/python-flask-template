app.controller('UserListCtrl', function(
  $scope,
  $state,
  users
) {
  $scope.users = users;

  $scope['delete'] = function(user) {
    console.log('delte called');
    user.$delete().then(function() {
      // Force reload regardless of params changing
      $state.reload(true);
    }, function(error) {
      console.error(error);
    });
  };
});
