app.controller('UserCreateCtrl', function(
  $scope,
  $state,
  resources,
  user
) {
  $scope.user = user;

  $scope.passwordsMatch = function() {
    return $scope.userCreateForm.confirmPassword.$touched && user.password === $scope.confirmPassword;
  }

  $scope.passwordsMismatch = function() {
    return $scope.userCreateForm.confirmPassword.$touched && user.password !== $scope.confirmPassword;
  }

  $scope.save = function() {
    resources.users.save($scope.user, function(user) {
      console.log('Created successfully');
      $state.go('users.list', {id: user.id});
    }, function(error) {
      console.error(error);
    });
  };
});
