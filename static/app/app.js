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
    console.error(error.stack);
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
    .state('table', {
      url: '/table',
      template: '<div ui-view></div>',
      redirect: 'table.list',
    })
    .state('table.list', {
      url: '/all',
      templateUrl: LIB_ROOT + 'TableList.tpl.html',
      controller: 'TableListCtrl',
      resolve: {
        tables: function(resources) {
          return resources.table.query().$promise;
        },
      }
    })
    .state('table.view', {
      url: '/:name',
      templateUrl: LIB_ROOT + 'TableView.tpl.html',
      controller: 'TableCtrl',
      resolve: {
        table: function($stateParams, resources) {
          return resources.table.get({ name: $stateParams.name }).$promise;
        },
      }
    })
  ;
});
