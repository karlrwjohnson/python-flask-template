var app = angular.module('thing', [
  'ui.router',
  'ngResource',
]);

app.constant('LIB_ROOT', 'static/app/');

// Log state changes
app.run(function($rootScope) {
  $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams) {
    console.log('$stateChangeStart: ' + fromState.name + ' -> ' + toState.name, toParams);
  });
  $rootScope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams) {
    console.log('$stateChangeSuccess: ' + fromState.name + ' -> ' + toState.name);
  });
  $rootScope.$on('$stateChangeError', function(event, toState, toParams, fromState, fromParams, error) {
    console.log('$stateChangeError: ' + fromState.name + ' -> ' + toState.name + '(', toParams, ')\n', error);
    console.error(error.stack || error);
  });
});

// Handle state redirects by hooking into UI Router
app.run(function($rootScope, $state) {
  $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams) {
    if ('redirect' in toState) {
      event.preventDefault();
      $state.go(toState.redirect, toParams);
    }
  });
});

// Configure navigation
app.config(function(
  $stateProvider,
  LIB_ROOT
) {
  'use strict';

  $stateProvider
    .state('null', {
      url: '',
      onEnter: function($state) {
        $state.go('root');
      }
    })
    .state('root', {
      url: '/',
      templateUrl: LIB_ROOT + 'Main.tpl.html',
    })
    .state('widgets', {
      url: '/widgets',
      template: '<div ui-view></div>',
      redirect: 'widgets.list',
    })
    .state('widgets.list', {
      url: '/all?{highlight}',
      templateUrl: LIB_ROOT + 'WidgetList.tpl.html',
      controller: 'WidgetListCtrl',
      resolve: {
        widgets: function(resources) {
          return resources.widgets.query().$promise;
        },
        highlight: function($stateParams) {
          console.log('highlight = ' + $stateParams.highlight);
          return ('highlight' in $stateParams) ?
            Number($stateParams.highlight) :
            null;
        },
      }
    })
    .state('widgets.new', {
      url: '/new',
      templateUrl: LIB_ROOT + 'WidgetEdit.tpl.html',
      controller: 'WidgetCtrl',
      resolve: {
        widget: function(resources) {
          return resources.widgets.new();
        },
      }
    })
    .state('widgets.view', {
      url: '/:id',
      templateUrl: LIB_ROOT + 'WidgetView.tpl.html',
      controller: 'WidgetCtrl',
      resolve: {
        widget: function($stateParams, resources) {
          return resources.widgets.get({ id: $stateParams.id }).$promise;
        },
      }
    })
    .state('widgets.edit', {
      url: '/:id/edit',
      templateUrl: LIB_ROOT + 'WidgetEdit.tpl.html',
      controller: 'WidgetCtrl',
      resolve: {
        widget: function($stateParams, resources) {
          return resources.widgets.get({ id: $stateParams.id }).$promise;
        },
      }
    })
    .state('users', {
      url: '/users',
      template: '<div ui-view></div>',
      redirect: 'users.list',
    })
    .state('users.list', {
      url: '/all',
      templateUrl: LIB_ROOT + 'UserList.tpl.html',
      controller: 'UserListCtrl',
      resolve: {
        users: function(resources) {
          return resources.users.query().$promise;
        },
      }
    })
    .state('users.new', {
      url: '/new',
      templateUrl: LIB_ROOT + 'UserCreate.tpl.html',
      controller: 'UserCreateCtrl',
      resolve: {
        user: function(resources) {
          return resources.users.new();
        },
      }
    })
  ;
});
